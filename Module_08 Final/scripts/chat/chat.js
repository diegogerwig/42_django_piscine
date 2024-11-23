const initChat = (roomName, username, initialMessageCount) => {
    let chatSocket = null;
    let messageCount = initialMessageCount || 0;
    let initialLoadComplete = false;
    const INITIAL_MESSAGES_TO_SHOW = 3;

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

    // Clear chat log with loading message
    function clearChatLog() {
        const chatLog = document.querySelector('#chat-log');
        if (chatLog) {
            chatLog.innerHTML = '<div class="text-center text-muted mt-3">Loading messages...</div>';
        }
    }

    // Execute clearChatLog before anything else
    document.addEventListener('DOMContentLoaded', clearChatLog);
    // Also clear immediately in case the script loads after DOMContentLoaded
    clearChatLog();

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
    }

    async function loadHistoricalMessages(loadAll = false) {
        if (initialLoadComplete && !loadAll) return;
        
        removeAllAlerts();
        
        try {
            // Show loading message
            clearChatLog();
            
            const response = await fetch(`/chat/api/${roomName}/messages/`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const messages = await response.json();
            
            // Filter user and system messages
            const userMessages = messages.filter(msg => msg.username !== 'System');
            const systemMessages = messages.filter(msg => msg.username === 'System');
            
            // Update total message count
            messageCount = userMessages.length;
            updateMessageCount(messageCount);

            // Add artificial delay of 1 second
            await new Promise(resolve => setTimeout(resolve, 1000));

            // Clear the chat log before adding new messages
            const chatLog = document.querySelector('#chat-log');
            chatLog.innerHTML = '';

            if (loadAll) {
                // Display all messages in chronological order
                messages.forEach(data => {
                    displayMessage(data);
                });
            } else {
                // Display only the last 3 user messages
                const lastUserMessages = userMessages.slice(-INITIAL_MESSAGES_TO_SHOW);
                lastUserMessages.forEach(data => {
                    displayMessage(data);
                });

                // Display the latest system message if it exists
                const lastSystemMessage = systemMessages[systemMessages.length - 1];
                if (lastSystemMessage) {
                    displayMessage(lastSystemMessage);
                }
            }
            
            scrollToBottom();
            initialLoadComplete = true;
            removeAllAlerts();
            
            // Update load history button state
            const loadHistoryBtn = document.getElementById('load-history-btn');
            if (loadHistoryBtn) {
                loadHistoryBtn.style.display = loadAll ? 'none' : 'inline-block';
            }
        } catch (error) {
            console.error('Error loading messages:', error);
            const chatLog = document.querySelector('#chat-log');
            chatLog.innerHTML = '<div class="text-center text-danger mt-3">Error loading messages. Please try again.</div>';
        }
    }

    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        chatSocket = new WebSocket(`${protocol}//${window.location.host}/ws/chat/${roomName}/`);

        chatSocket.onopen = function() {
            if (!initialLoadComplete) {
                loadHistoricalMessages(false);
            }
        }

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            displayMessage(data);
            
            if (data.username !== 'System') {
                messageCount++;
                updateMessageCount(messageCount);
            }
            scrollToBottom();
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
        const loadHistoryBtn = document.getElementById('load-history-btn');

        if (loadHistoryBtn) {
            loadHistoryBtn.addEventListener('click', () => loadHistoricalMessages(true));
        }

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