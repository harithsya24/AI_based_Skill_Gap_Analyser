function searchCourses() {
    let query = document.getElementById("searchQuery").value;
    if (!query) {
        alert("Please enter a search term.");
        return;
    }

    fetch(`/search_courses?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            let resultsList = document.getElementById("results");
            resultsList.innerHTML = ""; 

            if (data.courses.length === 0) {
                resultsList.innerHTML = "<li>No courses found.</li>";
                return;
            }

            data.courses.forEach(course => {
                let li = document.createElement("li");
                li.textContent = course.content;
                resultsList.appendChild(li);
            });
        })
        .catch(error => {
            console.error("Error fetching courses:", error);
            alert("Something went wrong, please try again later.");
        });
}
