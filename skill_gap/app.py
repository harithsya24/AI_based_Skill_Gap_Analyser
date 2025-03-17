from flask import Blueprint, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Define the blueprint for skill gap service
skills_test_bp = Blueprint("skills_test", __name__, template_folder="templates", static_folder="static")

# Load dataset
csv_file_path = os.path.join(os.path.dirname(__file__), "courses.csv")
df = pd.read_csv(csv_file_path)

required_columns = ["Name", "Link", "Difficulty Level"]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Warning: Missing columns in dataset: {missing_columns}")

def get_similar_courses(query):
    if df.empty:
        print("Error: Dataset is empty!")
        return []

    vectorizer = TfidfVectorizer(stop_words="english")
    course_names = df["Name"].astype(str).tolist()
    course_names.append(query)
    tfidf_matrix = vectorizer.fit_transform(course_names)
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    similar_indices = cosine_sim.argsort()[0][-5:][::-1]
    similar_courses = df.iloc[similar_indices][["Name", "Link", "Difficulty Level"]]
    similar_courses = similar_courses.rename(columns={
        "Name": "course_title",
        "Link": "course_url",
        "Difficulty Level": "rating"
    })
    return similar_courses.to_dict(orient="records")

# Routes for skill gap
@skills_test_bp.route("/")
def index():
    return render_template("course_search.html")

@skills_test_bp.route("/courses", methods=["POST"])
def show_courses():
    user_query = request.form.get("query", "").strip()
    if not user_query:
        return render_template("course_search.html", courses=[], message="Please enter a search query.")

    similar_courses = get_similar_courses(user_query)
    if not similar_courses:
        return render_template("courses.html", courses=[], message="No matching courses found.")

    return render_template("courses.html", courses=similar_courses)
