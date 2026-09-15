# CodeCraftHub

CodeCraftHub is a beginner-friendly course tracking REST API built with **Python** and **Flask**.

The application allows users to create, view, update, and delete courses. Course information is stored locally in `courses.json`, so no database setup is required.

This project is designed to demonstrate the basics of:

* REST APIs and HTTP methods
* JSON request and response data
* Flask routes
* CRUD operations
* File-based data storage
* HTTP status codes

---

## Features

* Create new courses
* View all courses
* View a course by ID
* Update existing courses
* Delete courses
* Automatically generate numeric course IDs
* Automatically generate creation timestamps
* Validate required fields and date formats
* Validate allowed course statuses
* Store course data in `courses.json`
* Automatically create `courses.json` if it does not exist
* Return JSON responses and error messages
* No authentication or database required

### Course Statuses

Every course must use one of the following status values:

* `Not Started`
* `In Progress`
* `Completed`

---

## Technologies Used

* Python 3
* Flask
* JSON
* `curl` for API testing

---

## Project Structure

```text
CodeCraftHub/
├── app.py
├── courses.json
├── requirements.txt
└── README.md
```

**`app.py`** — Contains the Flask application, API endpoints, validation logic, and JSON file handling.

**`courses.json`** — Stores all course data. It is automatically created when the application starts if it does not already exist.

**`requirements.txt`** — Lists the Python packages required by the project.

**`README.md`** — Contains project documentation and instructions.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/CodeCraftHub.git
cd CodeCraftHub
```

### 2. Create a Virtual Environment

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, Flask can be installed directly:

```bash
pip install Flask
```

---

## Running the Application

Start the Flask server:

**macOS/Linux:**

```bash
python3 app.py
```

**Windows:**

```bash
python app.py
```

You should see output similar to:

```text
Using course data file: /path/to/CodeCraftHub/courses.json
* Running on http://127.0.0.1:5000
```

The API will then be available at `http://127.0.0.1:5000`.

Keep the terminal running while testing the API. Press `CTRL+C` to stop the server.

---

## API Endpoints

| Method   | Endpoint            | Description        |
| -------- | ------------------- | ------------------ |
| `POST`   | `/api/courses`      | Add a new course   |
| `GET`    | `/api/courses`      | Get all courses    |
| `GET`    | `/api/courses/<id>` | Get a course by ID |
| `PUT`    | `/api/courses/<id>` | Update a course    |
| `DELETE` | `/api/courses/<id>` | Delete a course    |

The `<id>` should be replaced with a numeric course ID. For example:

```text
/api/courses/1
```

### Course Data Format

Creating or updating a course requires the following JSON:

```json
{
    "name": "Course name",
    "description": "Course description",
    "target_date": "YYYY-MM-DD",
    "status": "Not Started"
}
```

The `status` must be `Not Started`, `In Progress`, or `Completed`.

The server automatically generates:

* `id` — Numeric course ID
* `created_at` — UTC timestamp indicating when the course was created

---

## API Examples

### Create a Course

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "REST API Fundamentals",
    "description": "Learn HTTP methods, status codes, and REST API design.",
    "target_date": "2026-10-15",
    "status": "Not Started"
  }'
```

A successful request returns `201 CREATED`.

### Get All Courses

```bash
curl -i http://127.0.0.1:5000/api/courses
```

A successful request returns `200 OK`.

### Get a Course by ID

```bash
curl -i http://127.0.0.1:5000/api/courses/1
```

### Update a Course

```bash
curl -i -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Advanced REST API Design",
    "description": "Learn advanced API patterns, validation, and error handling.",
    "target_date": "2026-12-01",
    "status": "In Progress"
  }'
```

### Delete a Course

```bash
curl -i -X DELETE http://127.0.0.1:5000/api/courses/1
```

---

## HTTP Status Codes

| Status                      | Meaning                                         |
| --------------------------- | ----------------------------------------------- |
| `200 OK`                    | Request succeeded                               |
| `201 CREATED`               | A new resource was created                      |
| `400 BAD REQUEST`           | The request contains invalid data               |
| `404 NOT FOUND`             | The requested course or endpoint does not exist |
| `405 METHOD NOT ALLOWED`    | The HTTP method is not supported                |
| `500 INTERNAL SERVER ERROR` | A server or file error occurred                 |

---

## Error Handling

CodeCraftHub validates incoming course data and returns JSON error messages when a request is invalid.

For example, a request missing the `description` field returns:

```json
{
    "error": "Missing required field(s): description"
}
```

Other validation includes:

* Required fields
* Non-empty names and descriptions
* Dates in `YYYY-MM-DD` format
* Valid course statuses
* Existing course IDs
* Valid JSON request bodies

---

## Testing

The API can be tested using `curl` from a second terminal while the Flask server is running.

It can also be tested using Postman by selecting the appropriate HTTP method, entering the endpoint URL, and providing a JSON request body for `POST` and `PUT` requests.

---

## Resetting Test Data

To remove all courses, stop the Flask server and replace the contents of `courses.json` with:

```json
[]
```

Then restart the application.

---

## Troubleshooting

### Flask Is Not Installed

If you receive:

```text
ModuleNotFoundError: No module named 'flask'
```

install Flask with:

```bash
python3 -m pip install Flask
```

### Port 5000 Is Already in Use

Change the Flask port in `app.py`:

```python
app.run(debug=True, port=5001)
```

Then access the API at `http://127.0.0.1:5001`.

### `curl` Cannot Connect

Make sure:

* The Flask application is running.
* You are using the correct URL and port.
* The terminal running Flask is still open.

### Invalid JSON

JSON property names and string values must use double quotes:

```json
{
    "name": "Python Basics",
    "description": "Learn Python.",
    "target_date": "2026-10-20",
    "status": "Not Started"
}
```

### Invalid Course Status

The status must exactly match one of:

* `Not Started`
* `In Progress`
* `Completed`

### Invalid Date

Dates must use the `YYYY-MM-DD` format, such as:

```text
2026-10-15
```

---

## Important Notes

CodeCraftHub uses a JSON file instead of a database to keep the project simple and beginner-friendly. This approach works well for learning projects, personal projects, and small local applications.

For larger applications with many users or large amounts of data, a database such as SQLite or PostgreSQL would be more appropriate.

The application currently runs with Flask debug mode enabled. Debug mode is useful during development but should not be used in production.

CodeCraftHub does not include authentication or authorization. Anyone with access to the API can create, modify, or delete courses.
