document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");

    window.sendMessage = function() {
        const message = userInput.value.trim();
        if (message === "") return;

        appendMessage("You", message);

        fetch("/mentor/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage("AI Mentor", data.response);
        })
        .catch(error => {
            appendMessage("Error", "Failed to connect to AI.");
        });

        userInput.value = "";
    };

    function appendMessage(sender, message) {
        const msgDiv = document.createElement("div");
        msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
        msgDiv.classList.add("mb-2");
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
