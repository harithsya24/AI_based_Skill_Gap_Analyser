from flask import Flask, render_template, request, jsonify
import subprocess
import os
import logging

# Import blueprints for the services
from mentor.app import mentor_bp
from recomendation.app import recommendation_bp
from skill_gap.app import skills_test_bp

# Configure logging
logging.basicConfig(
    filename="service_logs.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize the Flask application
app = Flask(__name__, template_folder="templates")

# Register blueprints for each service
app.register_blueprint(mentor_bp, url_prefix="/mentor")
app.register_blueprint(recommendation_bp, url_prefix="/recommendation")
app.register_blueprint(skills_test_bp, url_prefix="/skills_test")

# Dictionary to manage processes for each service
processes = {}

def start_service(service):
    """ Start a service if not already running. """
    if service in processes and processes[service].poll() is None:
        logging.info(f"{service} is already running.")
        return f"{service} is already running."
    
    service_mapping = {
        "mentor": ["python", os.path.abspath("integrated/mentor/app.py")],
        "recommendation": ["python", os.path.abspath("integrated/recommendation/app.py")],
        "skills_test": ["python", os.path.abspath("integrated/skill_gap/app.py")]
    }
    
    if service in service_mapping:
        try:
            # Start the service if it's not already running
            processes[service] = subprocess.Popen(
                service_mapping[service],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logging.info(f"Started {service} successfully.")
            return f"{service} started successfully."
        except Exception as e:
            logging.error(f"Error starting {service}: {e}")
            return f"Error: Unable to start {service}."
    return "Invalid service."

# Define the route for the home page
@app.route("/")
def index():
    return render_template("index_main.html")

# Define the route for starting services
@app.route("/start_service", methods=["POST"])
def start_service_route():
    data = request.json
    service = data.get("service")
    if not service:
        return jsonify({"message": "No service specified."}), 400
    message = start_service(service)
    return jsonify({"message": message})

# Run the Flask app
if __name__ == "__main__":
    app.run(port=5000, debug=True)