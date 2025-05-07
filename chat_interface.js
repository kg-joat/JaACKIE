async function sendUserInput(userInput) {
    const chatContainer = document.getElementById("chat-container");
    const userMessage = document.createElement("div");

    // Add user message to the chat container
    userMessage.textContent = userInput;
    userMessage.classList.add("chat-bubble", "user");
    chatContainer.appendChild(userMessage);

    try {
        // Send user input to the backend
        const response = await fetch('/respond', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: userInput }),
        });
        const botResponse = await response.json();

        // Display bot response
        displayBotResponse(botResponse);
    } catch (error) {
        console.error('Error:', error);
        const botMessage = document.createElement("div");
        botMessage.textContent = "An error occurred while fetching the response.";
        botMessage.classList.add("chat-bubble", "bot");
        chatContainer.appendChild(botMessage);
    }
}

function displayBotResponse(responseObject) {
    const chatContainer = document.getElementById("chat-container");
    const botMessage = document.createElement("div");

    // Set the response text
    botMessage.textContent = responseObject.response;

    // Set the chat bubble color based on the mode
    if (responseObject.mode === "learning") {
        botMessage.style.backgroundColor = "#800080"; // Purple for learning mode
    } else {
        botMessage.style.backgroundColor = "#0000FF"; // Blue for normal chatting mode
    }

    // Add the bot message to the chat container
    botMessage.classList.add("chat-bubble", "bot");
    chatContainer.appendChild(botMessage);
}