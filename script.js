
const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const messages = document.getElementById("messages");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userMessage = input.value.trim();
    if (!userMessage) return;

    appendMessage("Tú", userMessage);
    input.value = "";
    appendMessage("Planetaquim", "...");

    try {
        const response = await fetch("https://planetaquim-backend.onrender.com/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        });

        const data = await response.json();
        const botMessage = data.response || "No he podido responder, ¿probamos otra vez?";
        messages.lastChild.remove(); // remove the "..." message
        appendMessage("Planetaquim", botMessage);
    } catch (error) {
        messages.lastChild.remove(); // remove the "..." message
        appendMessage("Planetaquim", "Ups... algo no ha funcionado bien.");
        console.error("Error:", error);
    }
});

function appendMessage(sender, text) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
    messages.appendChild(messageElement);
    messages.scrollTop = messages.scrollHeight;
}
