document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-log");
    const userInput = document.getElementById("user-input");

    window.sendMessage = function() {
        const message = userInput.value.trim();
        if (message === "") return;

        appendMessage("You", message, 'user-message');

        fetch("/mentor/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage("AI Mentor", data.response, 'ai-message');
        })
        .catch(error => {
            appendMessage("Error", "Failed to connect to AI.", 'ai-message');
        });

        userInput.value = "";
    };

    function appendMessage(sender, message, messageClass) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add(messageClass, 'mb-2');
        msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
