// chat-websocket.js
const initChatWebSocket = (roomName, username, chatCore) => {
    let chatSocket = null;
    let messageCount = 0;
    const MAX_RETRIES = 5;
    let reconnectCount = 0;
    window.isExplicitExit = false;

    function createLoadingOverlay() {
        const existingOverlay = document.getElementById('websocket-loading-overlay');
        if (existingOverlay) existingOverlay.remove();

        const overlay = document.createElement('div');
        overlay.id = 'websocket-loading-overlay';
        overlay.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center';
        overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.85)';
        overlay.style.zIndex = '9999';

        overlay.innerHTML = `
            <div class="card bg-dark border-secondary" style="max-width: 400px; width: 90%;">
                <div class="card-header bg-dark text-white border-secondary d-flex align-items-center">
                    <i class="bi bi-broadcast me-2"></i>
                    <h5 class="mb-0">WebSocket Connection Status</h5>
                </div>
                <div class="card-body">
                    <div class="connecting-state">
                        <div class="d-flex align-items-center p-3 mb-2 bg-dark border border-primary rounded">
                            <div class="spinner-border text-primary me-3" role="status">
                                <span class="visually-hidden">Connecting...</span>
                            </div>
                            <div class="text-primary">
                                Establishing WebSocket connection...
                            </div>
                        </div>
                    </div>
                    
                    <div class="connected-state d-none">
                        <div class="d-flex align-items-center p-3 mb-2 bg-dark border border-success rounded">
                            <i class="bi bi-check-circle-fill text-success me-3 fs-4"></i>
                            <div class="text-success">
                                WebSocket connected successfully!
                            </div>
                        </div>
                    </div>
                    
                    <div class="error-state d-none">
                        <div class="d-flex align-items-center p-3 mb-2 bg-dark border border-danger rounded">
                            <i class="bi bi-exclamation-triangle-fill text-danger me-3 fs-4"></i>
                            <div>
                                <div class="text-danger mb-2">
                                    Connection failed
                                </div>
                                <button onclick="window.location.reload()" 
                                        class="btn btn-danger btn-sm d-flex align-items-center">
                                    <i class="bi bi-arrow-repeat me-2"></i>
                                    Retry Connection
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);
        return overlay;
    }

    function updateLoadingState(state, message = '') {
        const overlay = document.getElementById('websocket-loading-overlay');
        if (!overlay) return;

        const connectingState = overlay.querySelector('.connecting-state');
        const connectedState = overlay.querySelector('.connected-state');
        const errorState = overlay.querySelector('.error-state');

        connectingState.classList.add('d-none');
        connectedState.classList.add('d-none');
        errorState.classList.add('d-none');

        switch(state) {
            case 'connecting':
                connectingState.classList.remove('d-none');
                break;
            case 'connected':
                connectedState.classList.remove('d-none');
                setTimeout(() => {
                    overlay.style.transition = 'opacity 0.5s ease-in-out';
                    overlay.style.opacity = '0';
                    setTimeout(() => overlay.remove(), 500);
                }, 1000);
                break;
            case 'error':
                errorState.classList.remove('d-none');
                if (message) {
                    const errorDiv = errorState.querySelector('.text-danger');
                    if (errorDiv) errorDiv.textContent = message;
                }
                break;
        }
    }

    function setupEventListeners() {
        const submitButton = document.getElementById('chat-message-submit');
        const messageInput = document.getElementById('chat-message-input');

        if (submitButton) {
            submitButton.onclick = handleMessageSubmit;
            // Make button larger and add padding
            submitButton.className = 'btn btn-success fs-5 px-4 ms-3';
        }

        if (messageInput) {
            // Add maxlength attribute to input
            messageInput.maxLength = 500;
            
            // Create a container for the counter
            const counterContainer = document.createElement('div');
            counterContainer.className = 'd-flex align-items-center';
            messageInput.parentNode.appendChild(counterContainer);

            // Create send button wrapper
            const buttonWrapper = document.createElement('div');
            buttonWrapper.className = 'me-3';
            
            // Move submit button to wrapper
            submitButton.parentNode.removeChild(submitButton);
            buttonWrapper.appendChild(submitButton);
            counterContainer.appendChild(buttonWrapper);
            
            // Add character counter
            const counterDiv = document.createElement('div');
            counterDiv.className = 'text-muted text-center mt-1';
            counterDiv.id = 'message-length-counter';

            // Initialize counter with 500
            counterDiv.innerHTML = `
                <span class="fs-5 fw-bold">500</span><br>
                <span class="small">characters<br>remaining</span>
            `;
            counterContainer.appendChild(counterDiv);

            // Update counter on input
            messageInput.addEventListener('input', function() {
                const remaining = 500 - this.value.length;
                counterDiv.innerHTML = `
                    <span class="fs-5 fw-bold">${remaining}</span><br>
                    <span class="small">characters<br>remaining</span>
                `;
                counterDiv.className = remaining === 0 ? 'text-danger text-center mt-1' : 
                        remaining < 50 ? 'text-warning text-center mt-1' : 
                        'text-muted text-center mt-1';
            });

            messageInput.onkeypress = function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleMessageSubmit();
                }
            };
            messageInput.focus();
        }
    }

    function handleMessageSubmit() {
        const messageInput = document.getElementById('chat-message-input');
        const message = messageInput.value.trim();
        const MAX_MESSAGE_LENGTH = 500; // Maximum characters allowed
        
        if (!message) return;
        
        if (message.length > MAX_MESSAGE_LENGTH) {
            alert(`Message is too long. Maximum ${MAX_MESSAGE_LENGTH} characters allowed. Current length: ${message.length}`);
            return;
        }

        if (!chatSocket || chatSocket.readyState !== WebSocket.OPEN) {
            alert('Connection lost. Please refresh the page.');
            return;
        }
        
        try {
            chatSocket.send(JSON.stringify({
                type: 'chat_message',
                message: message,
                room: roomName
            }));
            
            messageInput.value = '';
            const counterDiv = document.getElementById('message-length-counter');
            if (counterDiv) {
                counterDiv.innerHTML = `
                    <span class="fs-5 fw-bold">500</span><br>
                    <span class="small">characters<br>remaining</span>
                `;
                counterDiv.className = 'text-muted text-center mt-1';
            }
            chatCore.scrollToBottom();
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Error sending message. Please try again.');
        }
    }
    
    function connectWebSocket() {
        return new Promise((resolve, reject) => {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws/chat/${roomName}/`;
            
            try {
                chatSocket = new WebSocket(wsUrl);

                chatSocket.onopen = function() {
                    console.log('WebSocket connected successfully');
                    setupEventListeners();
                    updateLoadingState('connected');
                    resolve();
                };

                chatSocket.onmessage = function(e) {
                    try {
                        const data = JSON.parse(e.data);
                        console.log('Received message:', data);

                        // Handle new chat message
                        if (data.type === 'chat_message' || !data.type) {
                            // Always display the message
                            chatCore.displayMessage(data);

                            // Only update counter for non-system messages
                            if (data.username !== 'System') {
                                const countElement = document.getElementById(`message-count-${data.room || roomName}`);
                                if (countElement) {
                                    const currentText = countElement.textContent;
                                    const currentCount = parseInt(currentText) || 0;
                                    const newCount = currentCount + 1;
                                    chatCore.updateMessageCount(data.room || roomName, newCount);
                                }
                            }
                        }
                        // Handle user list updates
                        else if (data.type === 'user_list_update') {
                            chatCore.updateUserList(data.users);
                        }
                    } catch (error) {
                        console.error('Error processing message:', error);
                    }
                };

                chatSocket.onclose = function(e) {
                    console.log('WebSocket closed:', e.code, e.reason);
                    
                    if (e.code === 4000) {
                        window.isExplicitExit = true;
                        alert('Active session detected in another tab.');
                        window.location.href = '/logout/';
                        return;
                    }

                    if (!window.isExplicitExit && reconnectCount < MAX_RETRIES) {
                        reconnectCount++;
                        setTimeout(() => connectWebSocket(), 3000);
                        updateLoadingState('connecting', `Reconnecting... Attempt ${reconnectCount}/${MAX_RETRIES}`);
                    } else {
                        updateLoadingState('error', 'Connection lost. Please refresh to try again.');
                    }
                };

                chatSocket.onerror = function(error) {
                    console.error('WebSocket error:', error);
                    updateLoadingState('error', 'Connection error occurred');
                    reject(error);
                };

            } catch (error) {
                console.error('Error creating WebSocket:', error);
                updateLoadingState('error', 'Failed to create WebSocket connection');
                reject(error);
            }
        });
    }

    // Initialize
    console.log('Initializing chat WebSocket...');
    createLoadingOverlay();
    updateLoadingState('connecting');

    connectWebSocket()
        .then(() => {
            console.log('Chat WebSocket initialized successfully');
        })
        .catch(error => {
            console.error('Failed to initialize chat WebSocket:', error);
            updateLoadingState('error', 'Failed to connect to chat server');
        });

    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        window.isExplicitExit = true;
        if (chatSocket?.readyState === WebSocket.OPEN) {
            chatSocket.close();
        }
    });
};

window.initChatWebSocket = initChatWebSocket;