document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    addMessage('you', message);

    fetch('/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: message })
    })
    .then(response => response.json())
    .then(data => {
        addMessage('bot', data.response);
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('bot', '[Error fetching response]');
    });

    input.value = '';
}

function addMessage(sender, text) {
    const chatBox = document.getElementById('chat-box');
    const messageEl = document.createElement('div');
    messageEl.classList.add('message', sender);
    messageEl.textContent = text;
    chatBox.appendChild(messageEl);
    chatBox.scrollTop = chatBox.scrollHeight;
}