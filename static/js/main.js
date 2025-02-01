/**
 * Constants for error messages and configuration
 */
const ERRORS = {
    NETWORK: 'Network error occurred. Please check your connection.',
    TIMEOUT: 'Request timed out. Please try again.',
    SERVER: 'Server error occurred. Please try again later.',
    RATE_LIMIT: 'Too many messages. Please wait a moment.',
    MAX_LENGTH: 'Message is too long. Please shorten it.'
};

const CONFIG = {
    MAX_MESSAGE_LENGTH: 2000,
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000,
    FADE_DURATION: 300
};

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    let isLoading = false;

    /**
     * Add a message to the chat interface
     * @param {string} content - The message content to display
     * @param {boolean} isUser - Whether the message is from the user (true) or assistant (false)
     * @param {boolean} isError - Whether the message is an error message
     */
    function addMessage(content, isUser = false, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'assistant-message'} ${isError ? 'error-message' : ''}`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = formatTimestamp(new Date());

        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(timeDiv);

        // Add with fade-in effect
        messageDiv.style.opacity = '0';
        chatMessages.appendChild(messageDiv);
        setTimeout(() => {
            messageDiv.style.opacity = '1';
        }, 10);

        // Scroll to bottom with smooth animation
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }

    /**
     * Format timestamp in a readable format
     * @param {Date} date - The date to format
     * @returns {string} Formatted timestamp
     */
    function formatTimestamp(date) {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }

    /**
     * Set the loading state of the chat interface
     * @param {boolean} loading - Whether to show loading state
     */
    function setLoading(loading) {
        isLoading = loading;
        const submitButton = chatForm.querySelector('button[type="submit"]');
        submitButton.disabled = loading;
        messageInput.disabled = loading;

        if (loading) {
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message assistant-message loading';
            loadingDiv.id = 'loading-message';
            loadingDiv.setAttribute('aria-label', 'Loading response...');
            chatMessages.appendChild(loadingDiv);
            chatMessages.scrollTo({
                top: chatMessages.scrollHeight,
                behavior: 'smooth'
            });
        } else {
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                loadingMessage.remove();
            }
        }
    }

    /**
     * Send a message to the server with retry logic
     * @param {string} message - The message to send
     * @param {number} retryCount - Current retry attempt number
     * @returns {Promise<Object>} Server response
     */
    async function sendMessageWithRetry(message, retryCount = 0) {
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Request-ID': crypto.randomUUID()
                },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) {
                const data = await response.json();
                if (response.status === 429) {
                    throw new Error(ERRORS.RATE_LIMIT);
                }
                throw new Error(data.error || ERRORS.SERVER);
            }

            return await response.json();
        } catch (error) {
            if (retryCount < CONFIG.MAX_RETRIES &&
                error.message !== ERRORS.RATE_LIMIT) {
                await new Promise(resolve =>
                    setTimeout(resolve, CONFIG.RETRY_DELAY * (retryCount + 1))
                );
                return sendMessageWithRetry(message, retryCount + 1);
            }
            throw error;
        }
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const message = messageInput.value.trim();
        if (!message || isLoading) return;

        // Validate message length
        if (message.length > CONFIG.MAX_MESSAGE_LENGTH) {
            addMessage(ERRORS.MAX_LENGTH, false, true);
            return;
        }

        // Add user message to chat
        addMessage(message, true);
        messageInput.value = '';

        // Show loading state
        setLoading(true);

        try {
            const data = await sendMessageWithRetry(message);
            if (data.status === 'success') {
                addMessage(data.response);
            } else {
                throw new Error(data.error || ERRORS.SERVER);
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage(error.message, false, true);
        } finally {
            setLoading(false);
        }
    });

    // Initialize
    messageInput.focus();

    // Add character counter
    messageInput.addEventListener('input', () => {
        const length = messageInput.value.length;
        if (length > CONFIG.MAX_MESSAGE_LENGTH) {
            messageInput.classList.add('invalid');
        } else {
            messageInput.classList.remove('invalid');
        }
    });
});
