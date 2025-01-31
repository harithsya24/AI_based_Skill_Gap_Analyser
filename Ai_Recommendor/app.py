from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__, template_folder="../frontend/templates")

df = pd.read_csv("courses.csv")

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

@app.route("/")
def index():
    print("Index route accessed.")
    return render_template("course_search.html")

@app.route("/courses", methods=["POST"])
def show_courses():
    user_query = request.form.get("query", "").strip()

    if not user_query:
        print("Empty query received. Redirecting to index.")
        return render_template("course_search.html", courses=[], message="Please enter a search query.")

    similar_courses = get_similar_courses(user_query)

    if not similar_courses:
        print(f"No matches found for query: {user_query}")
        return render_template("courses.html", courses=[], message="No matching courses found.")

    print(f"Query processed: {user_query}. Results found: {len(similar_courses)}")
    return render_template("courses.html", courses=similar_courses)

if __name__ == "__main__":
    print("Starting Flask application...")
    app.run(port=5007)
    print("Flask application has stopped.")  
