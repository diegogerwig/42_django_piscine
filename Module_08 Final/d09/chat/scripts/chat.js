const initChat = (roomName, username, initialMessageCount) => {
    let chatSocket = null;
    let messageCount = initialMessageCount || 0;
    let initialLoadComplete = false;
    let userListInterval = null;
    const INITIAL_MESSAGES_TO_SHOW = 3;
    const WEBSOCKET_RECONNECT_BASE_DELAY = 1000;
    const MAX_RECONNECT_DELAY = 30000;
    const MAX_RETRIES = 5;
    const HEARTBEAT_INTERVAL = 30000;
    const PONG_TIMEOUT = 10000;
    let heartbeatTimer = null;
    let lastPongReceived = Date.now();
    let reconnectCount = 0;
    window.isExplicitExit = false;

    function removeAllAlerts() {
        const alerts = document.querySelectorAll('.alert, .alert-info, .alert-dismissible, div[role="alert"], .toast');
        alerts.forEach(alert => {
            alert.style.display = 'none';
            alert.remove();
        });
    }

    function setupAlertPrevention() {
        if (window.bootstrap) {
            bootstrap.Alert = function() { return null; };
            if (bootstrap.alert) bootstrap.alert = function() { return null; };
        }

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

        setInterval(removeAllAlerts, 50);
        document.addEventListener('DOMContentLoaded', removeAllAlerts);
        window.addEventListener('load', removeAllAlerts);
        document.addEventListener('readystatechange', removeAllAlerts);
    }

    function clearChatLog() {
        const chatLog = document.querySelector('#chat-log');
        if (chatLog) {
            chatLog.innerHTML = '<div class="text-center text-muted mt-3">Loading messages...</div>';
        }
    }

    function updateUserList(users) {
        const userListElement = document.getElementById('users-list');
        if (!userListElement) return;

        const sortedUsers = users.sort((a, b) => {
            if (a.is_online !== b.is_online) {
                return b.is_online - a.is_online;
            }
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
                ${isCurrentUser ? '(you)' : ''}
            `;
            userListElement.appendChild(userItem);
        });
    }

    function startHeartbeat() {
        stopHeartbeat();
        heartbeatTimer = setInterval(() => {
            if (chatSocket?.readyState === WebSocket.OPEN) {
                chatSocket.send(JSON.stringify({ type: 'ping' }));
                
                if (Date.now() - lastPongReceived > PONG_TIMEOUT) {
                    console.log('Pong timeout - reconnecting WebSocket');
                    reconnectWebSocket();
                }
            }
        }, HEARTBEAT_INTERVAL);
    }

    function stopHeartbeat() {
        if (heartbeatTimer) {
            clearInterval(heartbeatTimer);
            heartbeatTimer = null;
        }
    }

    function updateMessageCount(count) {
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

    async function loadHistoricalMessages(loadAll = false) {
        if (initialLoadComplete && !loadAll) return;
        
        removeAllAlerts();
        
        try {
            clearChatLog();
            
            const response = await fetch(`/chat/api/${roomName}/messages/`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const messages = await response.json();
            
            const userMessages = messages.filter(msg => msg.username !== 'System');
            const systemMessages = messages.filter(msg => msg.username === 'System');
            
            messageCount = userMessages.length;
            updateMessageCount(messageCount);

            await new Promise(resolve => setTimeout(resolve, 1000));

            const chatLog = document.querySelector('#chat-log');
            chatLog.innerHTML = '';

            if (loadAll) {
                messages.forEach(data => {
                    displayMessage(data);
                });
            } else {
                const lastUserMessages = userMessages.slice(-INITIAL_MESSAGES_TO_SHOW);
                lastUserMessages.forEach(data => {
                    displayMessage(data);
                });

                const lastSystemMessage = systemMessages[systemMessages.length - 1];
                if (lastSystemMessage) {
                    displayMessage(lastSystemMessage);
                }
            }
            
            scrollToBottom();
            initialLoadComplete = true;
            removeAllAlerts();
            
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

    function reconnectWebSocket() {
        if (chatSocket) {
            chatSocket.close();
        }
        connectWebSocket();
    }

    function getReconnectDelay() {
        const baseDelay = WEBSOCKET_RECONNECT_BASE_DELAY * Math.pow(2, reconnectCount);
        const jitter = Math.random() * 1000;
        return Math.min(baseDelay + jitter, MAX_RECONNECT_DELAY);
    }

    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';

        try {
            if (chatSocket && chatSocket.readyState !== WebSocket.CLOSED) {
                chatSocket.close();
            }

            chatSocket = new WebSocket(`${protocol}//${window.location.host}/ws/chat/${roomName}/`);

            chatSocket.onopen = function() {
                console.log("WebSocket connected successfully");
                reconnectCount = 0;
                lastPongReceived = Date.now();
                startHeartbeat();
                if (!initialLoadComplete) {
                    loadHistoricalMessages(false);
                }
            };

            chatSocket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                
                if (data.type === 'pong') {
                    lastPongReceived = Date.now();
                    return;
                }

                if (data.type === 'user_list_update') {
                    updateUserList(data.users);
                } else {
                    displayMessage(data);
                    if (data.username !== 'System') {
                        messageCount++;
                        updateMessageCount(messageCount);
                    }
                }
            };

            chatSocket.onclose = function(e) {
                stopHeartbeat();
                
                if (e.code === 4000) {
                    window.isExplicitExit = true;
                    alert('You cannot connect because you already have an active session in another browser/tab.');
                    window.location.href = '/logout/';
                    return;
                }

                if (!window.isExplicitExit && reconnectCount < MAX_RETRIES && e.code !== 1000) {
                    reconnectCount++;
                    const delay = getReconnectDelay();
                    console.log(`Attempting reconnect ${reconnectCount}/${MAX_RETRIES} in ${delay}ms`);
                    setTimeout(connectWebSocket, delay);
                }
            };

            chatSocket.onerror = function(error) {
                console.error('WebSocket error details:', {
                    readyState: chatSocket.readyState,
                    error: error
                });
            };

        } catch (error) {
            console.error('Error creating WebSocket:', error);
            if (!window.isExplicitExit && reconnectCount < MAX_RETRIES) {
                reconnectCount++;
                setTimeout(connectWebSocket, getReconnectDelay());
            }
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
        // Setup chat controls
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

        // Setup exit handling
        const logoutBtn = document.querySelector('button[type="submit"][class*="btn-danger"]');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                window.isExplicitExit = true;
            });
        }

        const roomLinks = document.querySelectorAll('a[href^="/chat/room/"]');
        roomLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (link.getAttribute('href') !== `/chat/room/${roomName}/`) {
                    window.isExplicitExit = true;
                }
            });
        });
    }

    window.addEventListener('beforeunload', () => {
        stopHeartbeat();
        if (window.isExplicitExit && chatSocket?.readyState === WebSocket.OPEN) {
            chatSocket.send(JSON.stringify({
                'type': 'user_offline'
            }));
        }
    });

    setupAlertPrevention();
    connectWebSocket();
    setupEventListeners();
};

window.initChat = initChat;