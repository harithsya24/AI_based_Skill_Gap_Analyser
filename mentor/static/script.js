function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== "") {
        var chatLog = document.getElementById('chat-log');
        chatLog.innerHTML += "<p><strong>You:</strong> " + userInput + "</p>";
        document.getElementById('user-input').value = "";  

        document.getElementById('user-input').disabled = true;
        document.querySelector('button').disabled = true; 

        fetch("/mentor/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput })
        })
        .then(response => response.json())
        .then(data => {
            chatLog.innerHTML += "<p><strong>AI Mentor:</strong> " + data.response + "</p>";
            chatLog.scrollTop = chatLog.scrollHeight;

            document.getElementById('user-input').disabled = false;
            document.querySelector('button').disabled = false;
        })
        .catch(error => {
            console.log("Error:", error);
            chatLog.innerHTML += "<p><strong>AI Mentor:</strong> Sorry, something went wrong.</p>";
            chatLog.scrollTop = chatLog.scrollHeight;

            document.getElementById('user-input').disabled = false;
            document.querySelector('button').disabled = false;
        });
    }
}

function startVoiceInput() {
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.start();

    recognition.onresult = function(event) {
        var transcript = event.results[0][0].transcript;
        document.getElementById('user-input').value = transcript;
        sendMessage();  
    };

    recognition.onerror = function(event) {
        console.log("Voice input error: " + event.error);
        alert("Voice input failed. Please try again.");
    };
}