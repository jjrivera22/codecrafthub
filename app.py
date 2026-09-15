"""
CodeCraftHub - Course Tracking REST API

This Flask application provides CRUD operations for courses.

Data is stored in a local JSON file named courses.json.
No database or authentication is required.
"""

from datetime import datetime
from pathlib import Path
import json
import os
import tempfile

from flask import Flask, jsonify, request
from flask_cors import CORS


# Create the Flask application
app = Flask(__name__)
CORS(app)

# Store courses.json in the same directory as this Python file
DATA_FILE = Path(__file__).resolve().parent / "courses.json"

# Allowed course status values
VALID_STATUSES = {
    "Not Started",
    "In Progress",
    "Completed"
}


# -------------------------------------------------------------------
# Helper functions for reading and writing courses.json
# -------------------------------------------------------------------

def create_data_file_if_missing():
    """
    Create courses.json automatically if it does not exist.

    The file starts with an empty JSON array because courses will be
    stored as a list of objects.
    """
    if not DATA_FILE.exists():
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def read_courses():
    """
    Read and return all courses from courses.json.

    Returns:
        list: A list of course dictionaries

    Raises:
        FileNotFoundError: If the file does not exist
        PermissionError: If the file cannot be read
        json.JSONDecodeError: If the file contains invalid JSON
        OSError: For other file-related errors
    """
    create_data_file_if_missing()

    with DATA_FILE.open("r", encoding="utf-8") as file:
        courses = json.load(file)

    # Make sure the JSON file contains a list
    if not isinstance(courses, list):
        raise ValueError("courses.json must contain a JSON list")

    return courses


def write_courses(courses):
    """
    Save all courses to courses.json.

    A temporary file is used first. Once writing succeeds, it replaces
    the original file. This helps reduce the chance of leaving behind
    a partially written JSON file.

    Args:
        courses (list): List of course dictionaries

    Raises:
        PermissionError: If the file cannot be written
        OSError: For other file-related errors
    """
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    temporary_file_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=DATA_FILE.parent,
            delete=False
        ) as temporary_file:
            json.dump(courses, temporary_file, indent=4)
            temporary_file.write("\n")
            temporary_file_path = temporary_file.name

        # Replace courses.json with the completed temporary file
        os.replace(temporary_file_path, DATA_FILE)

    except Exception:
        # Remove the temporary file if something went wrong
        if temporary_file_path and os.path.exists(temporary_file_path):
            os.remove(temporary_file_path)

        raise


# -------------------------------------------------------------------
# Helper functions for validation and responses
# -------------------------------------------------------------------

def get_request_data():
    """
    Get JSON data from the request body.

    Returns:
        tuple:
            - data dictionary or None
            - error response or None
    """
    data = request.get_json(silent=True)

    if data is None:
        return None, (
            jsonify({
                "error": "Request body must contain valid JSON"
            }),
            400
        )

    if not isinstance(data, dict):
        return None, (
            jsonify({
                "error": "Request JSON must be an object"
            }),
            400
        )

    return data, None


def validate_course_data(data):
    """
    Validate all required course fields.

    This function is used when creating a course and when replacing
    a course with PUT.

    Returns:
        str or None: An error message, or None if the data is valid
    """
    required_fields = [
        "name",
        "description",
        "target_date",
        "status"
    ]

    # Check whether all required fields exist
    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return (
            "Missing required field(s): "
            + ", ".join(missing_fields)
        )

    # Check that text fields are non-empty strings
    for field in ["name", "description"]:
        if not isinstance(data[field], str) or not data[field].strip():
            return f"{field} must be a non-empty string"

    # Check the target date format
    if not isinstance(data["target_date"], str):
        return "target_date must be a string in YYYY-MM-DD format"

    try:
        datetime.strptime(data["target_date"], "%Y-%m-%d")
    except ValueError:
        return "target_date must use the YYYY-MM-DD format"

    # Check that the status is one of the allowed values
    if data["status"] not in VALID_STATUSES:
        return (
            "Invalid status. Status must be one of: "
            + ", ".join(sorted(VALID_STATUSES))
        )

    return None


def get_next_course_id(courses):
    """
    Generate the next numeric course ID.

    IDs start at 1. If no courses exist, the next ID is 1.
    Otherwise, the next ID is one higher than the largest existing ID.
    """
    if not courses:
        return 1

    existing_ids = [
        course.get("id", 0)
        for course in courses
        if isinstance(course.get("id"), int)
    ]

    if not existing_ids:
        return 1

    return max(existing_ids) + 1


def get_course_by_id(courses, course_id):
    """
    Find a course by its numeric ID.

    Returns:
        dict or None: The matching course, if found
    """
    for course in courses:
        if course.get("id") == course_id:
            return course

    return None


def file_error_response(error):
    """
    Create a consistent response for file read/write errors.
    """
    app.logger.error("File error: %s", error)

    return jsonify({
        "error": "Unable to read or write courses.json"
    }), 500


# -------------------------------------------------------------------
# API endpoints
# -------------------------------------------------------------------

@app.get("/")
def home():
    return jsonify({
        "message": "CodeCraftHub Course Tracking API",
        "endpoint": "/api/courses"
    })

@app.post("/api/courses")
def add_course():
    """
    Add a new course.

    Endpoint:
        POST /api/courses
    """
    data, error_response = get_request_data()

    if error_response:
        return error_response

    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    try:
        courses = read_courses()

        now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

        new_course = {
            "id": get_next_course_id(courses),
            "name": data["name"].strip(),
            "description": data["description"].strip(),
            "target_date": data["target_date"],
            "status": data["status"],
            "created_at": now
        }

        courses.append(new_course)
        write_courses(courses)

        return jsonify(new_course), 201

    except (OSError, ValueError, json.JSONDecodeError) as error:
        return file_error_response(error)


@app.get("/api/courses")
def get_all_courses():
    """
    Get all courses.

    Endpoint:
        GET /api/courses
    """
    try:
        courses = read_courses()

        return jsonify(courses), 200

    except (OSError, ValueError, json.JSONDecodeError) as error:
        return file_error_response(error)


@app.get("/api/courses/<int:course_id>")
def get_specific_course(course_id):
    """
    Get one course by ID.

    Endpoint:
        GET /api/courses/<id>
    """
    try:
        courses = read_courses()
        course = get_course_by_id(courses, course_id)

        if course is None:
            return jsonify({
                "error": "Course not found"
            }), 404

        return jsonify(course), 200

    except (OSError, ValueError, json.JSONDecodeError) as error:
        return file_error_response(error)


@app.put("/api/courses/<int:course_id>")
def update_course(course_id):
    """
    Replace an existing course.

    PUT requires all editable course fields:
        - name
        - description
        - target_date
        - status

    The id and created_at fields are preserved.

    Endpoint:
        PUT /api/courses/<id>
    """
    data, error_response = get_request_data()

    if error_response:
        return error_response

    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    try:
        courses = read_courses()
        course = get_course_by_id(courses, course_id)

        if course is None:
            return jsonify({
                "error": "Course not found"
            }), 404

        # Update only the editable fields
        course["name"] = data["name"].strip()
        course["description"] = data["description"].strip()
        course["target_date"] = data["target_date"]
        course["status"] = data["status"]

        write_courses(courses)

        return jsonify(course), 200

    except (OSError, ValueError, json.JSONDecodeError) as error:
        return file_error_response(error)


@app.delete("/api/courses/<int:course_id>")
def delete_course(course_id):
    """
    Delete a course by ID.

    Endpoint:
        DELETE /api/courses/<id>
    """
    try:
        courses = read_courses()
        course = get_course_by_id(courses, course_id)

        if course is None:
            return jsonify({
                "error": "Course not found"
            }), 404

        courses.remove(course)
        write_courses(courses)

        return jsonify({
            "message": "Course deleted successfully",
            "course": course
        }), 200

    except (OSError, ValueError, json.JSONDecodeError) as error:
        return file_error_response(error)


# -------------------------------------------------------------------
# General application error handlers
# -------------------------------------------------------------------

@app.errorhandler(404)
def handle_not_found(error):
    """
    Return JSON instead of Flask's default HTML 404 response.
    """
    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def handle_method_not_allowed(error):
    """
    Return JSON when an unsupported HTTP method is used.
    """
    return jsonify({
        "error": "HTTP method not allowed"
    }), 405


@app.errorhandler(500)
def handle_internal_server_error(error):
    """
    Return JSON for unexpected server errors.
    """
    return jsonify({
        "error": "An unexpected server error occurred"
    }), 500


# -------------------------------------------------------------------
# Start the application
# -------------------------------------------------------------------

if __name__ == "__main__":
    # Create courses.json when the application starts.
    try:
        create_data_file_if_missing()
        print(f"Using course data file: {DATA_FILE}")
    except OSError as error:
        print(f"Warning: Could not create courses.json: {error}")

    # debug=True is useful while learning and developing.
    # Set debug=False for production use.
    app.run(debug=True)