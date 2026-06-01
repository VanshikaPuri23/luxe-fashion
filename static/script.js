function toggleChat() {
  const chatWindow = document.getElementById('chatWindow');
  chatWindow.classList.toggle('open');
}

async function sendMessage() {
  const input = document.getElementById('chatInput');
  const messages = document.getElementById('chatMessages');
  const text = input.value.trim();

  if (!text) return;
  input.value = '';

  // Add user message
  const userMsg = document.createElement('div');
  userMsg.className = 'msg user';
  userMsg.textContent = text;
  messages.appendChild(userMsg);

  // Add typing indicator
  const typing = document.createElement('div');
  typing.className = 'msg bot typing';
  typing.textContent = 'Typing...';
  messages.appendChild(typing);
  messages.scrollTop = messages.scrollHeight;

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });

    const data = await response.json();
    typing.remove();

    // Add bot reply
    const botMsg = document.createElement('div');
    botMsg.className = 'msg bot';
    botMsg.textContent = data.reply;
    messages.appendChild(botMsg);

  } catch (error) {
    typing.remove();
    const errMsg = document.createElement('div');
    errMsg.className = 'msg bot';
    errMsg.textContent = 'Sorry, something went wrong. Please try again!';
    messages.appendChild(errMsg);
  }

  messages.scrollTop = messages.scrollHeight;
}

// Send message on Enter key
document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('chatInput');
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') sendMessage();
  });
});