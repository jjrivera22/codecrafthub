# CodeCraftHub

CodeCraftHub is a beginner-friendly course tracking web application built with **Python**, **Flask**, **JavaScript**, and **Vite**.

The application allows users to create, view, update, and delete courses through a web interface. Course information is handled by a Flask REST API and stored locally in `courses.json`, so no database setup is required.

This project demonstrates the basics of:

- REST APIs and HTTP methods
- Frontend and backend communication
- JSON request and response data
- Flask routes
- CRUD operations
- JavaScript `fetch()` requests
- File-based data storage
- HTTP status codes

---

## Features

- Add courses through a web interface
- View all saved courses
- Edit existing courses
- Delete courses
- Track course status and target dates
- Automatically generate numeric course IDs
- Automatically generate creation timestamps
- Validate required fields and date formats
- Validate allowed course statuses
- Store course data in `courses.json`
- Automatically create `courses.json` if it does not exist
- Return JSON responses and error messages
- REST API can also be accessed directly
- No authentication or database required

### Course Statuses

Every course must use one of the following status values:

- `Not Started`
- `In Progress`
- `Completed`

---

## Technologies Used

- Python 3
- Flask
- Flask-CORS
- JavaScript
- HTML
- CSS
- Vite
- Node.js / npm
- JSON
- `curl` for API testing

---

## Project Structure

```text
codecrafthub/
├── public/
├── app.py
├── courses.json
├── index.html
├── main.js
├── style.css
├── counter.js
├── package.json
├── package-lock.json
├── requirements.txt
└── README.md
```

`app.py` — Contains the Flask backend, API endpoints, validation logic, and JSON file handling.

`courses.json` — Stores all course data.

`index.html` — Contains the CodeCraftHub web interface and frontend logic used to communicate with the Flask API.

`package.json` — Contains the frontend dependencies and Vite commands.

`requirements.txt` — Contains the Python dependencies required by the Flask backend.

`README.md` — Contains project documentation and setup instructions.

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/jjrivera22/codecrafthub.git
cd codecrafthub
```

## 2. Create a Python Virtual Environment

Creating a virtual environment is recommended so the project's Python packages do not interfere with other Python installations.

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Install the Python Dependencies

### macOS/Linux

```bash
python3 -m pip install -r requirements.txt
```

### Windows

```bash
python -m pip install -r requirements.txt
```

## 4. Install the Frontend Dependencies

Node.js and npm must be installed before running this command.

```bash
npm install
```

This installs the packages required by the Vite frontend.

---

# Running CodeCraftHub

CodeCraftHub uses **two separate servers**:

- Flask runs the backend API on port `5000`.
- Vite runs the frontend website on port `5173`.

**Both servers must be running at the same time for the website to work correctly.**

## 1. Start the Flask Backend

Open a terminal in the `codecrafthub` directory.

### macOS/Linux

```bash
python3 app.py
```

### Windows

```bash
python app.py
```

You should see output similar to:

```text
Using course data file: /path/to/codecrafthub/courses.json
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

**Leave this terminal running.**

You can verify that the backend is working by opening the following address in a browser:

```text
http://127.0.0.1:5000/api/courses
```

If the API is working, you should see the courses stored in `courses.json`.

For example:

```json
[
  {
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2025-12-31",
    "status": "Not Started",
    "created_at": "2026-09-15T02:57:00Z"
  }
]
```

If there are no courses yet, the API may return:

```json
[]
```

## 2. Start the Vite Frontend

Open a **second terminal**.

Navigate to the same `codecrafthub` directory and run:

```bash
npm run dev
```

You should see output similar to:

```text
VITE ready

➜  Local: http://localhost:5173/
```

**Leave this terminal running too.**

## 3. Open the Website

Open the following address in your browser:

```text
http://localhost:5173/
```

The CodeCraftHub interface should now appear.

You can use the website to:

- Add courses
- View courses
- Edit courses
- Change course statuses
- Delete courses

Changes made through the website are sent to the Flask API and stored in `courses.json`.

## Important: Keep Both Terminals Running

While using CodeCraftHub, you should have **two terminals running at the same time**:

```text
Terminal 1 — Flask Backend

python3 app.py

Running at:
http://127.0.0.1:5000
```

```text
Terminal 2 — Vite Frontend

npm run dev

Running at:
http://localhost:5173
```

If the Flask server is stopped, the website may still appear, but it will not be able to load, create, edit, or delete courses.

If the Vite server is stopped, `http://localhost:5173/` will not load.

Press `CTRL+C` in either terminal when you want to stop that server.

---

# API Endpoints

The Flask backend can also be accessed directly without using the website.

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/courses` | Add a new course |
| `GET` | `/api/courses` | Get all courses |
| `GET` | `/api/courses/<id>` | Get a course by ID |
| `PUT` | `/api/courses/<id>` | Update a course |
| `DELETE` | `/api/courses/<id>` | Delete a course |

The `<id>` should be replaced with a numeric course ID.

For example:

```text
/api/courses/1
```

## Course Data Format

Creating or updating a course requires JSON in the following format:

```json
{
  "name": "Course name",
  "description": "Course description",
  "target_date": "YYYY-MM-DD",
  "status": "Not Started"
}
```

The `status` must be:

- `Not Started`
- `In Progress`
- `Completed`

The server automatically generates:

- `id` — Numeric course ID
- `created_at` — UTC timestamp indicating when the course was created

---

# API Examples

The following examples can be run from another terminal while the Flask backend is running.

## Create a Course

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

## Get All Courses

```bash
curl -i http://127.0.0.1:5000/api/courses
```

A successful request returns `200 OK`.

## Get a Course by ID

```bash
curl -i http://127.0.0.1:5000/api/courses/1
```

## Update a Course

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

## Delete a Course

```bash
curl -i -X DELETE http://127.0.0.1:5000/api/courses/1
```

---

# HTTP Status Codes

| Status | Meaning |
| --- | --- |
| `200 OK` | Request succeeded |
| `201 CREATED` | A new resource was created |
| `400 BAD REQUEST` | The request contains invalid data |
| `404 NOT FOUND` | The requested course or endpoint does not exist |
| `405 METHOD NOT ALLOWED` | The HTTP method is not supported |
| `500 INTERNAL SERVER ERROR` | A server or file error occurred |

---

# Error Handling

CodeCraftHub validates incoming course data and returns JSON error messages when a request is invalid.

For example, a request missing the `description` field returns:

```json
{
  "error": "Missing required field(s): description"
}
```

Other validation includes:

- Required fields
- Non-empty names and descriptions
- Dates in `YYYY-MM-DD` format
- Valid course statuses
- Existing course IDs
- Valid JSON request bodies

---

# Testing

The easiest way to test the complete application is through the web interface:

```text
http://localhost:5173/
```

The API can also be tested directly using `curl` while the Flask server is running.

It can also be tested using Postman by selecting the appropriate HTTP method, entering the API endpoint, and providing a JSON request body for `POST` and `PUT` requests.

---

# Resetting Test Data

To remove all saved courses:

1. Stop the Flask server.
2. Open `courses.json`.
3. Replace its contents with:

```json
[]
```

4. Save the file.
5. Restart Flask:

```bash
python3 app.py
```

6. Refresh the frontend.

---

# Troubleshooting

## `localhost:5173` Cannot Be Reached

The Vite frontend is probably not running.

Open a terminal in the project directory and run:

```bash
npm run dev
```

Keep that terminal open while using CodeCraftHub.

---

## Website Says "Failed to Fetch"

First, make sure the Flask backend is running:

```bash
python3 app.py
```

Then open this address directly in your browser:

```text
http://127.0.0.1:5000/api/courses
```

If Flask is working, you should see JSON containing the saved courses.

The frontend expects the API at:

```text
http://127.0.0.1:5000/api/courses
```

Also make sure the terminal running Flask remains open.

---

## `npm` Command Not Found

Node.js and npm are required to run the frontend.

Verify whether they are installed:

```bash
node --version
npm --version
```

If you are using macOS and Homebrew, Node.js can be installed with:

```bash
brew install node
```

Then run:

```bash
npm install
npm run dev
```

---

## Flask Is Not Installed

If you receive:

```text
ModuleNotFoundError: No module named 'flask'
```

install the project's Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

---

## `flask_cors` Is Not Installed

If you receive:

```text
ModuleNotFoundError: No module named 'flask_cors'
```

install Flask-CORS:

```bash
python3 -m pip install flask-cors
```

Make sure `flask-cors` is also included in `requirements.txt`.

---

## Port 5000 Is Already in Use

Flask normally runs on port `5000`.

If you change the Flask server to another port, you must also update the `API_URL` in the frontend so that both sides use the same port.

For example, if Flask uses port `5001`:

```python
app.run(debug=True, port=5001)
```

the frontend API URL must also use port `5001`:

```javascript
const API_URL = 'http://127.0.0.1:5001/api/courses';
```

---

## API Works but the Website Does Not

First check the backend directly:

```text
http://127.0.0.1:5000/api/courses
```

If that works, make sure Vite is also running:

```bash
npm run dev
```

Then access the website through:

```text
http://localhost:5173/
```

Do not use the Flask API URL as the main website. Port `5000` is the backend, while port `5173` is the frontend.

---

## `curl` Cannot Connect

Make sure:

- The Flask application is running.
- You are using `http://127.0.0.1:5000`.
- The terminal running Flask is still open.

---

## Invalid JSON

JSON property names and string values must use double quotes:

```json
{
  "name": "Python Basics",
  "description": "Learn Python.",
  "target_date": "2026-10-20",
  "status": "Not Started"
}
```

---

## Invalid Course Status

The status must exactly match one of:

- `Not Started`
- `In Progress`
- `Completed`

---

## Invalid Date

Dates must use the `YYYY-MM-DD` format, such as:

```text
2026-10-15
```

---

# Important Notes

CodeCraftHub uses a JSON file instead of a database to keep the project simple and beginner-friendly. This approach works well for learning projects, personal projects, and small local applications.

The frontend and backend run separately during development. Vite serves the website on port `5173`, while Flask serves the REST API on port `5000`.

For larger applications with many users or large amounts of data, a database such as SQLite or PostgreSQL would be more appropriate.

The application currently runs with Flask debug mode enabled. Debug mode is useful during development but should not be used in production.

CodeCraftHub does not include authentication or authorization. Anyone with access to the API can create, modify, or delete courses.