// Microsoft Copilot-style Chat functionality
const copilotWelcome = document.getElementById('copilotWelcome');
const chatInterface = document.getElementById('chatInterface');
const chatMessages = document.getElementById('chatMessages');
const centerInputField = document.getElementById('centerInputField');
const centerSendBtn = document.getElementById('centerSendBtn');
const chatInputField = document.getElementById('chatInputField');
const chatSendBtn = document.getElementById('chatSendBtn');
const newChatBtn = document.getElementById('newChatBtn');
const notification = document.getElementById('notification');
const notificationText = document.getElementById('notificationText');

let chatHistory = [];
let isTyping = false;
let isFirstMessage = true;

// Initialize the interface
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    setupSuggestions();
});

function setupEventListeners() {
    // Center input field (welcome screen)
    centerInputField.addEventListener('input', () => {
        autoResize(centerInputField);
        centerSendBtn.disabled = !centerInputField.value.trim();
    });

    centerInputField.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessageFromCenter();
        }
    });

    centerSendBtn.addEventListener('click', sendMessageFromCenter);

    // Chat input field (chat interface)
    chatInputField.addEventListener('input', () => {
        autoResize(chatInputField);
        chatSendBtn.disabled = !chatInputField.value.trim();
    });

    chatInputField.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessageFromChat();
        }
    });

    chatSendBtn.addEventListener('click', sendMessageFromChat);

    // New chat button
    newChatBtn.addEventListener('click', startNewChat);
}

function setupSuggestions() {
    const suggestions = document.querySelectorAll('.suggestion-item');
    suggestions.forEach(suggestion => {
        suggestion.addEventListener('click', () => {
            const text = suggestion.getAttribute('data-text');
            centerInputField.value = text;
            centerSendBtn.disabled = false;
            autoResize(centerInputField);
        });
    });
}

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

async function sendMessageFromCenter() {
    const message = centerInputField.value.trim();
    if (!message || isTyping) return;

    // Transition to chat interface
    await transitionToChatInterface();
    
    // Send the message
    await sendMessage(message);
    
    // Clear center input
    centerInputField.value = '';
    centerSendBtn.disabled = true;
}

async function sendMessageFromChat() {
    const message = chatInputField.value.trim();
    if (!message || isTyping) return;

    await sendMessage(message);
    
    // Clear chat input
    chatInputField.value = '';
    chatSendBtn.disabled = true;
    autoResize(chatInputField);
}

async function transitionToChatInterface() {
    return new Promise((resolve) => {
        copilotWelcome.classList.add('exiting');
        
        setTimeout(() => {
            copilotWelcome.classList.add('hidden');
            chatInterface.classList.remove('hidden');
            chatInterface.classList.add('entering');
            
            setTimeout(() => {
                chatInterface.classList.remove('entering');
                resolve();
            }, 400);
        }, 400);
    });
}

async function sendMessage(message) {
    isTyping = true;
    
    // Add user message
    addMessage(message, 'user');
    
    // Add typing indicator
    const typingId = addTypingIndicator();
    
    try {
        console.log('🚀 Sending message to server:', message);
        console.log('📚 Chat history:', chatHistory);
        
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: chatHistory
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('📨 Received response from server:', data);
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add assistant response
        addMessage(data.response || 'Sorry, I couldn\'t process that request.', 'assistant');
        
        // Update chat history
        chatHistory.push({
            user: message,
            response: data.response
        });

    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator(typingId);
        addMessage('Sorry, there was an error processing your request. Please try again.', 'assistant');
        showNotification('Connection error. Please check your network.');
    }
    
    isTyping = false;
}

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    // Add avatar
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    if (sender === 'user') {
        avatar.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-3.3137 3.134-6 8-6s8 2.6863 8 6v1H4v-1z"/></svg>';
    } else {
        avatar.innerHTML = '🤖'; // Bot icon
    }
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (sender === 'assistant') {
        // Parse markdown for assistant messages and wrap tables
        let htmlContent = marked.parse(content);
        // Wrap tables in scrollable containers with proper styling
        htmlContent = htmlContent.replace(/<table>/g, '<div class="table-container"><table>');
        htmlContent = htmlContent.replace(/<\/table>/g, '</table></div>');
        messageContent.innerHTML = htmlContent;
    } else {
        messageContent.textContent = content;
    }
    
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    
    messageDiv.appendChild(avatar);
    const contentWrapper = document.createElement('div');
    contentWrapper.style.flex = '1';
    
    // For user messages, put content wrapper before avatar (so avatar appears on right)
    if (sender === 'user') {
        contentWrapper.style.display = 'flex';
        contentWrapper.style.flexDirection = 'column';
        contentWrapper.style.alignItems = 'flex-end';
        messageDiv.insertBefore(contentWrapper, avatar);
    } else {
        messageDiv.appendChild(contentWrapper);
    }
    
    contentWrapper.appendChild(messageContent);
    contentWrapper.appendChild(timestamp);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTypingIndicator() {
    const typingId = `typing-${Date.now()}`;
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = typingId;
    
    // Add bot avatar
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = '🤖';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const loadingDots = document.createElement('div');
    loadingDots.className = 'loading-dots';
    loadingDots.innerHTML = '<div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div>';
    
    messageContent.appendChild(loadingDots);
    
    messageDiv.appendChild(avatar);
    const contentWrapper = document.createElement('div');
    contentWrapper.style.flex = '1';
    contentWrapper.appendChild(messageContent);
    messageDiv.appendChild(contentWrapper);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return typingId;
}

function removeTypingIndicator(typingId) {
    const typingElement = document.getElementById(typingId);
    if (typingElement) {
        typingElement.remove();
    }
}

function startNewChat() {
    chatHistory = [];
    chatMessages.innerHTML = '';
    
    // Transition back to welcome screen
    chatInterface.classList.add('hidden');
    copilotWelcome.classList.remove('hidden', 'exiting');
    
    // Reset input fields
    centerInputField.value = '';
    chatInputField.value = '';
    centerSendBtn.disabled = true;
    chatSendBtn.disabled = true;
    
    showNotification('Started new chat');
}

function showNotification(message) {
    notificationText.textContent = message;
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Auto-focus on center input when page loads
window.addEventListener('load', () => {
    centerInputField.focus();
});
