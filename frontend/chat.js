const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const statusText = document.getElementById("statusText");
const replyText = document.getElementById("replyText");

const sessionId = crypto.randomUUID();

async function sendMessage() {
    const messageText = messageInput.value.trim();

    if (!messageText) {
        return;
    }

    sendButton.disabled = true;
    messageInput.disabled = true;
    statusText.textContent = "Ждём ответ…";

    try {
        const serverResponse = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: messageText,
                session_id: sessionId,
                region: "Удмуртская Республика",
                city: "Ижевск"
            })
        });

        if (!serverResponse.ok) {
            throw new Error("Сервер вернул ошибку " + serverResponse.status);
        }

        const responseData = await serverResponse.json();

        if (!responseData.reply) {
            throw new Error("ИИ не вернул текст ответа.");
        }

        replyText.textContent = responseData.reply;
        messageInput.value = "";
        statusText.textContent = "";

    } catch (error) {
        statusText.textContent = "Не удалось получить ответ. " + error.message;

    } finally {
        sendButton.disabled = false;
        messageInput.disabled = false;
    }
}

sendButton.addEventListener("click", sendMessage);