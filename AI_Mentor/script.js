document.getElementById("sendBtn").addEventListener("click", async function () {
    let userMessage = document.getElementById("userInput").value.trim();
    let chatBox = document.getElementById("chat-log");

    if (!userMessage) return;
    let userBubble = `<div class="d-flex justify-content-end"><div class="user-bubble">${userMessage}</div></div>`;
    chatBox.innerHTML += userBubble;
    document.getElementById("userInput").value = ""; 
    chatBox.scrollTop = chatBox.scrollHeight; 

    let typingIndicator = document.createElement("div");
    typingIndicator.id = "typing";
    typingIndicator.innerHTML = `<div class="d-flex justify-content-start"><div class="ai-bubble">AI is typing...</div></div>`;
    chatBox.appendChild(typingIndicator);
    chatBox.scrollTop = chatBox.scrollHeight; 

    await new Promise(r => setTimeout(r, 500));

    try {
        let response = await fetch("/mentor/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        });

        let data = await response.json();
        
        typingIndicator.remove();

        if (data.response) {
            let aiBubble = `<div class="d-flex justify-content-start"><div class="ai-bubble">${data.response}</div></div>`;
            chatBox.innerHTML += aiBubble;
        } else {
            chatBox.innerHTML += `<div class="d-flex justify-content-start"><div class="ai-bubble">Error: ${data.error || "Unknown error"}</div></div>`;
        }
    } catch (error) {
        typingIndicator.remove();
        chatBox.innerHTML += `<div class="d-flex justify-content-start"><div class="ai-bubble">Failed to connect.</div></div>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
});
