// chat-core.js
const initChatCore = (roomName, username) => {
    let messageCount = 0;
    let initialLoadComplete = false;
    const INITIAL_MESSAGES_TO_SHOW = 3;

    function clearChatLog() {
        const chatLog = document.querySelector('#chat-log');
        if (chatLog) {
            chatLog.innerHTML = `
                <div class="text-center text-muted mt-3">
                    <div class="spinner-border spinner-border-sm me-2" role="status">
                        <span class="visually-hidden">Loading messages...</span>
                    </div>
                    Loading messages...
                </div>`;
        }
    }

    function updateUserList(users) {
        const userListElement = document.getElementById('users-list');
        if (!userListElement) return;

        const sortedUsers = users.sort((a, b) => {
            if (a.is_online !== b.is_online) return b.is_online - a.is_online;
            return a.username.localeCompare(b.username);
        });

        userListElement.innerHTML = '';
        sortedUsers.forEach(user => {
            const userItem = document.createElement('div');
            userItem.className = 'list-group-item bg-secondary text-light border-secondary';
            const isCurrentUser = user.username === username;
            
            userItem.innerHTML = `
                <span class="text-${user.is_online ? 'success' : 'secondary'} me-2">●</span>
                ${user.username}
                ${isCurrentUser ? '<span class="ms-1 text-muted">(you)</span>' : ''}
            `;
            userListElement.appendChild(userItem);
        });
    }

    function updateMessageCount(roomName, count) {
        const countElement = document.getElementById(`message-count-${roomName}`);
        if (countElement) {
            countElement.textContent = `${count} message${count !== 1 ? 's' : ''}`;
        }
    }

    function scrollToBottom() {
        const container = document.querySelector('#chat-messages-container');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }

    function displayMessage(data) {
        const chatLog = document.querySelector('#chat-log');
        if (!chatLog) return;

        const isSystem = data.username === 'System';
        const isCurrentUser = data.username === username;
        
        const messageElement = document.createElement('div');
        
        if (isSystem) {
            messageElement.className = 'text-center mb-3';
            messageElement.innerHTML = `
                <div class="text-muted small">
                    ${data.message}
                    <span class="ms-2">${data.timestamp}</span>
                </div>
            `;
        } else {
            // Ensure message length is within limits even if backend validation fails
            const MAX_DISPLAY_LENGTH = 500;
            let displayMessage = data.message;
            let truncated = false;

            if (displayMessage.length > MAX_DISPLAY_LENGTH) {
                displayMessage = displayMessage.substring(0, MAX_DISPLAY_LENGTH);
                truncated = true;
            }

            messageElement.className = `mb-3 ${isCurrentUser ? 'text-end' : ''}`;
            messageElement.innerHTML = `
                <div class="d-flex align-items-baseline ${isCurrentUser ? 'justify-content-end' : ''}">
                    <strong class="me-2 ${isCurrentUser ? 'text-success' : 'text-info'}">${data.username}</strong>
                    <small class="text-muted">${data.timestamp}</small>
                </div>
                <div class="d-inline-block bg-secondary text-light rounded p-2 mt-1" 
                    style="max-width: 90%; overflow-wrap: break-word; word-wrap: break-word; hyphens: auto; white-space: pre-line;">
                    ${displayMessage}
                    ${truncated ? '<div class="text-warning small mt-1">Message was truncated due to length</div>' : ''}
                </div>
            `;
        }
        
        chatLog.appendChild(messageElement);
        scrollToBottom();
    }

    async function loadHistoricalMessages(loadAll = false) {
        try {
            clearChatLog();
            
            const response = await fetch(`/chat/api/${roomName}/messages/`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const messages = await response.json();
            const userMessages = messages.filter(msg => msg.username !== 'System');
            
            const chatLog = document.querySelector('#chat-log');
            chatLog.innerHTML = '';

            if (loadAll) {
                messages.forEach(data => displayMessage(data));
            } else {
                // Show only last 3 user messages
                const lastUserMessages = userMessages.slice(-INITIAL_MESSAGES_TO_SHOW);
                lastUserMessages.forEach(data => displayMessage(data));
            }
            
            // Update message count only with user messages
            updateMessageCount(roomName, userMessages.length);
            
            scrollToBottom();
            initialLoadComplete = true;
            
            const loadHistoryBtn = document.getElementById('load-history-btn');
            if (loadHistoryBtn) {
                loadHistoryBtn.style.display = loadAll ? 'none' : 'inline-block';
            }
        } catch (error) {
            console.error('Error loading messages:', error);
            const chatLog = document.querySelector('#chat-log');
            chatLog.innerHTML = `
                <div class="text-center text-danger mt-3">
                    <i class="bi bi-exclamation-circle me-2"></i>
                    Error loading messages. Please try again.
                </div>`;
        }
    }

    // Load initial messages immediately
    loadHistoricalMessages(false);

    return {
        displayMessage,
        updateUserList,
        updateMessageCount,
        loadHistoricalMessages,
        scrollToBottom,
        clearChatLog
    };
};

window.initChatCore = initChatCore;