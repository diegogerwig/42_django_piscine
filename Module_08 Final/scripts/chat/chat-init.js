// chat-init.js
window.ChatApp = {
    initialized: false,
    websocketStatus: 'disconnected',
    core: null,
    socket: null,
    overlay: null
};

const initChat = (roomName, username, initialMessageCount) => {
    console.log('Starting chat initialization...', {
        room: roomName,
        user: username,
        messageCount: initialMessageCount
    });

    // Prevent multiple initializations
    if (window.ChatApp.initialized) {
        console.warn('Chat already initialized');
        return;
    }

    // Basic validation
    if (!roomName || !username) {
        console.error('Missing required parameters for chat initialization');
        return;
    }

    try {
        // Initialize the chat core first
        console.log('Initializing chat core...');
        window.ChatApp.core = initChatCore(roomName, username);

        if (!window.ChatApp.core) {
            throw new Error('Failed to initialize chat core');
        }

        // Initialize WebSocket with a small delay to ensure DOM is ready
        console.log('Preparing WebSocket initialization...');
        setTimeout(() => {
            try {
                window.ChatApp.socket = initChatWebSocket(roomName, username, window.ChatApp.core)
                    .then(() => {
                        window.ChatApp.initialized = true;
                        window.ChatApp.websocketStatus = 'connected';
                        console.log('Chat fully initialized and connected');
                    })
                    .catch(error => {
                        console.error('WebSocket initialization failed:', error);
                        window.ChatApp.websocketStatus = 'error';
                    });
            } catch (error) {
                console.error('Error during WebSocket initialization:', error);
                window.ChatApp.websocketStatus = 'error';
            }
        }, 500);

        // Setup error handlers
        window.onerror = function(message, source, lineno, colno, error) {
            console.error('Global error caught:', {
                message,
                source,
                lineno,
                colno,
                error
            });
            return false;
        };

        // Setup unload handler
        window.addEventListener('beforeunload', () => {
            if (window.ChatApp.initialized) {
                console.log('Cleaning up chat resources...');
                window.ChatApp.websocketStatus = 'disconnected';
                window.ChatApp.initialized = false;
            }
        });

        // Setup load history button handler
        const loadHistoryBtn = document.getElementById('load-history-btn');
        if (loadHistoryBtn) {
            loadHistoryBtn.addEventListener('click', () => {
                if (window.ChatApp.core) {
                    window.ChatApp.core.loadHistoricalMessages(true);
                }
            });
        }

    } catch (error) {
        console.error('Critical error during chat initialization:', error);
        window.ChatApp.websocketStatus = 'error';
        // Optionally show error to user
        if (document.getElementById('chat-log')) {
            document.getElementById('chat-log').innerHTML = `
                <div class="alert alert-danger text-center">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    Failed to initialize chat. Please refresh the page.
                </div>
            `;
        }
    }
};

// Debug helper function
window.ChatApp.debug = {
    getStatus: () => {
        return {
            initialized: window.ChatApp.initialized,
            websocketStatus: window.ChatApp.websocketStatus,
            coreLoaded: !!window.ChatApp.core,
            socketLoaded: !!window.ChatApp.socket
        };
    },
    reinitialize: () => {
        window.ChatApp.initialized = false;
        window.ChatApp.websocketStatus = 'disconnected';
        window.ChatApp.core = null;
        window.ChatApp.socket = null;
        window.location.reload();
    }
};

// Make initialization function globally available
window.initChat = initChat;

// Auto-initialize if data is available in window
document.addEventListener('DOMContentLoaded', () => {
    if (!window.chatInitData) {
        console.warn('Chat initialization data not found');
        return;
    }

    console.log('Starting chat with data:', window.chatInitData);
    
    const { roomName, username, messageCount } = window.chatInitData;
    if (!roomName || !username) {
        console.error('Missing required chat parameters');
        return;
    }

    // Small delay to ensure all resources are loaded
    setTimeout(() => {
        initChat(roomName, username, messageCount);
    }, 100);
});

// Export for module systems if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { initChat };
}