const initChat = (roomName, username, initialMessageCount) => {
    let chatSocket = null;
    let messageCount = initialMessageCount || 0;
    let initialLoadComplete = false;

    // Function to ensure no alerts exist
    function removeAllAlerts() {
        const alerts = document.querySelectorAll('.alert, .alert-info, .alert-dismissible, div[role="alert"], .toast');
        alerts.forEach(alert => {
            alert.style.display = 'none';
            alert.remove();
        });
    }

    // Remove alerts aggressively
    function setupAlertPrevention() {
        // Override Bootstrap's alert creation
        if (window.bootstrap) {
            bootstrap.Alert = function() { return null; };
            if (bootstrap.alert) bootstrap.alert = function() { return null; };
        }

        // Set up observer for dynamic content
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.addedNodes && mutation.addedNodes.length > 0) {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1 && node.tagName === 'DIV') {
                            if (node.classList && 
                                (node.classList.contains('alert') || 
                                 node.classList.contains('alert-info') ||
                                 node.classList.contains('alert-dismissible') ||
                                 node.getAttribute('role') === 'alert')) {
                                node.style.display = 'none';
                                node.remove();
                            }
                        }
                    });
                }
            });
            removeAllAlerts();
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['class', 'role']
        });

        // Set interval for continuous checking
        setInterval(removeAllAlerts, 50);

        // Remove alerts on any dynamic content changes
        document.addEventListener('DOMContentLoaded', removeAllAlerts);
        window.addEventListener('load', removeAllAlerts);
        document.addEventListener('readystatechange', removeAllAlerts);
    }

    function updateMessageCount(count) {
        const countElement = document.getElementById(`message-count-${roomName}`);
        if (countElement) {
            countElement.textContent = `${count} message${count !== 1 ? 's' : ''}`;
        }
    }

    function scrollToBottom() {
        const container = document.querySelector('#chat-messages-container');
        container.scrollTop = container.scrollHeight;
    }

    function displayMessage(data) {
        const chatLog = document.querySelector('#chat-log');
        const isSystem = data.username === 'System';
        const isCurrentUser = data.username === username;
        
        const messageElement = document.createElement('div');
        
        if (isSystem) {
            messageElement.className = 'message mb-2 text-center';
            messageElement.innerHTML = `
                <div class="text-muted">
                    ${data.message}
                    <small>${data.timestamp}</small>
                </div>
            `;
        } else {
            messageElement.className = `message mb-2 ${isCurrentUser ? 'text-end' : ''}`;
            messageElement.innerHTML = `
                <div class="d-flex align-items-baseline ${isCurrentUser ? 'justify-content-end' : ''}">
                    <strong class="me-2 ${isCurrentUser ? 'text-success' : 'text-info'}">${data.username}</strong>
                    <small class="text-muted">${data.timestamp}</small>
                </div>
                <div class="message-content text-light">
                    ${data.message}
                </div>
            `;
        }
        
        chatLog.appendChild(messageElement);
        scrollToBottom();
    }

    async function loadHistoricalMessages() {
        if (initialLoadComplete) return;
        
        removeAllAlerts();
        
        try {
            const response = await fetch(`/chat/api/${roomName}/messages/`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const messages = await response.json();
            const chatLog = document.querySelector('#chat-log');
            chatLog.innerHTML = '';
            
            let userMessageCount = 0;
            
            messages.forEach(data => {
                displayMessage(data);
                if (data.username !== 'System') {
                    userMessageCount++;
                }
            });
            
            messageCount = userMessageCount;
            updateMessageCount(messageCount);
            scrollToBottom();
            initialLoadComplete = true;
            removeAllAlerts();
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }

    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        chatSocket = new WebSocket(`${protocol}//${window.location.host}/ws/chat/${roomName}/`);

        chatSocket.onopen = function() {
            if (!initialLoadComplete) {
                loadHistoricalMessages();
            }
        }

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            displayMessage(data);
            
            if (data.username !== 'System') {
                messageCount++;
                updateMessageCount(messageCount);
            }
        }

        chatSocket.onclose = function() {
            setTimeout(connectWebSocket, 3000);
        }

        chatSocket.onerror = function(error) {
            console.error('WebSocket error:', error);
        }
    }

    function handleMessageSubmit() {
        const messageInput = document.getElementById('chat-message-input');
        const message = messageInput.value.trim();
        
        if (message && chatSocket && chatSocket.readyState === WebSocket.OPEN) {
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInput.value = '';
            scrollToBottom();
        }
    }

    function setupEventListeners() {
        const submitButton = document.getElementById('chat-message-submit');
        const messageInput = document.getElementById('chat-message-input');

        if (submitButton) {
            submitButton.addEventListener('click', handleMessageSubmit);
        }

        if (messageInput) {
            messageInput.addEventListener('keyup', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    handleMessageSubmit();
                }
            });
            messageInput.focus();
        }
    }

    // Initialize immediately instead of waiting for window.load
    setupAlertPrevention();
    connectWebSocket();
    setupEventListeners();
};

// Make sure initChat is available globally
window.initChat = initChat;