const roomName = "{{ room.name }}";
const username = "{{ user.username }}";
let chatSocket;

function connectWebSocket() {
	// Usar el protocolo correcto (ws o wss)
	const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	const wsUrl = protocol + '//' + window.location.host + '/ws/chat/' + roomName + '/';
	
	console.log('Connecting to WebSocket at:', wsUrl);
	chatSocket = new WebSocket(wsUrl);

	chatSocket.onopen = function(e) {
		console.log('WebSocket connection established');
	};

	chatSocket.onmessage = function(e) {
		console.log('Message received:', e.data);
		const data = JSON.parse(e.data);
		const messageElement = document.createElement('div');
		const isCurrentUser = data.username === username;
		
		messageElement.className = `message mb-2 ${isCurrentUser ? 'text-end' : ''}`;
		messageElement.innerHTML = `
			<div class="d-flex align-items-baseline ${isCurrentUser ? 'justify-content-end' : ''}">
				<strong class="me-2 ${isCurrentUser ? 'text-success' : 'text-primary'}">${data.username}</strong>
				<small class="text-muted">${data.timestamp || new Date().toLocaleTimeString().slice(0, 5)}</small>
			</div>
			<div class="message-content text-light">
				${data.message}
			</div>
		`;
		
		const chatLog = document.querySelector('#chat-log');
		chatLog.appendChild(messageElement);
		chatLog.scrollTop = chatLog.scrollHeight;
	};

	chatSocket.onclose = function(e) {
		console.log('WebSocket connection closed. Attempting to reconnect...');
		setTimeout(connectWebSocket, 3000);
	};

	chatSocket.onerror = function(e) {
		console.error('WebSocket error:', e);
	};
}

connectWebSocket();

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
	if (e.key === 'Enter' && !e.shiftKey) {
		document.querySelector('#chat-message-submit').click();
		e.preventDefault();
	}
};

document.querySelector('#chat-message-submit').onclick = function(e) {
	const messageInputDom = document.querySelector('#chat-message-input');
	const message = messageInputDom.value.trim();
	if (message && chatSocket.readyState === WebSocket.OPEN) {
		console.log('Sending message:', message);
		chatSocket.send(JSON.stringify({
			'message': message
		}));
		messageInputDom.value = '';
	}
};

// Auto scroll to bottom on load
document.addEventListener('DOMContentLoaded', function() {
	const chatLog = document.querySelector('#chat-log');
	chatLog.scrollTop = chatLog.scrollHeight;
});