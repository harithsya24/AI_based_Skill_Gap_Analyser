# AI Based Skill Gap Analyzer

This project is a Flask-based web application that serves as a platform for managing and displaying various functionalities, including serving templates, handling data, and providing AI-driven features. The application also integrates with various APIs and leverages machine learning models for some of its core features.

## Features

- **Flask Web Framework**: A lightweight and scalable web application framework for building modern web applications.
- **Template Rendering**: Dynamically render HTML templates with the Jinja templating engine.
- **AI Integration**: Fetches data from APIs and uses AI for content generation.
- **Debug Mode**: Detailed error logging in the development environment.

## Project Structure

### Backend (`/backend/`)

- **`app.py`**: Main Flask application entry point. Contains route handling, app configuration, and application initialization.
- **`config.py`**: Configuration file to store sensitive information like API keys and other settings.
- **`data/`**: Stores data in JSON format, like fetched news, user preferences, or AI-generated content.
- **`utils/`**: Utility functions for web scraping, interacting with APIs, or performing necessary background tasks.
- **`static/`**: Stores static files like JavaScript, CSS, and images used by the frontend.

### Frontend (`/frontend/`)

- **`templates/`**: HTML templates used by Flask's `render_template` function to render content.
- **`static/`**: CSS and JavaScript files used to build the UI.
  - **`css/`**: Stylesheets to style the website using Bootstrap or custom styles.
  - **`js/`**: JavaScript files for frontend interactivity and data fetching.

### Other Files

- **`.env`**: Environment variables for sensitive information like API keys.
- **`requirements.txt`**: List of Python dependencies needed to run the project.
- **`README.md`**: Project documentation for developers and users.

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    ```

3. **Activate the virtual environment**:
    - For macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    - For Windows:
        ```bash
        venv\Scripts\activate
        ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Set environment variables** (Optional, if needed):
    - Create a `.env` file in the root directory to store any sensitive configuration details like API keys.
    - Example:
        ```
        GOOGLE_API_KEY=your-api-key
        FLASK_SECRET_KEY=your-flask-secret-key
        ```

6. **Run the Flask app**:
    ```bash
    python3 app.py
    ```

7. **Access the app**:
    - Open a web browser and visit `http://127.0.0.1:5000/`.

## Development

For local development, ensure that the Flask app runs with the `debug=True` flag, which allows detailed error logging and hot-reloading of the application during development.

### Example Route
```python
@app.route('/')
def index():
    return render_template("index_main.html")
