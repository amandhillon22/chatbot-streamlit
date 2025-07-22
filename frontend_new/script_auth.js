// Authentication and Chat functionality
let currentUser = null;
let currentSessionId = null;
let chatHistory = [];
let isTyping = false;
let isFirstMessage = true;

// DOM Elements
const loginContainer = document.getElementById('loginContainer');
const mainContainer = document.getElementById('mainContainer');
const loginForm = document.getElementById('loginForm');
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const copilotWelcome = document.getElementById('copilotWelcome');
const chatInterface = document.getElementById('chatInterface');
const chatMessages = document.getElementById('chatMessages');
const centerInputField = document.getElementById('centerInputField');
const centerSendBtn = document.getElementById('centerSendBtn');
const chatInputField = document.getElementById('chatInputField');
const chatSendBtn = document.getElementById('chatSendBtn');
const newChatBtn = document.getElementById('newChatBtn');
const newChatBtnSidebar = document.getElementById('newChatBtnSidebar');
const chatSessions = document.getElementById('chatSessions');
const userName = document.getElementById('userName');
const logoutBtn = document.getElementById('logoutBtn');
const notification = document.getElementById('notification');
const notificationText = document.getElementById('notificationText');

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuthentication();
    setupEventListeners();
    setupSuggestions();
});

// Check if user is already authenticated
async function checkAuthentication() {
    try {
        const response = await fetch('/api/user');
        const data = await response.json();
        
        if (data.authenticated) {
            currentUser = data.user;
            showMainInterface();
            await loadChatSessions();
        } else {
            showLoginInterface();
        }
    } catch (error) {
        console.error('Authentication check failed:', error);
        showLoginInterface();
    }
}

function showLoginInterface() {
    loginContainer.classList.remove('hidden');
    mainContainer.classList.add('hidden');
}

function showMainInterface() {
    loginContainer.classList.add('hidden');
    mainContainer.classList.remove('hidden');
    userName.textContent = currentUser.username;
}

function setupEventListeners() {
    // Login form
    loginForm.addEventListener('submit', handleLogin);
    
    // Logout button
    logoutBtn.addEventListener('click', handleLogout);
    
    // Sidebar toggle
    sidebarToggle.addEventListener('click', toggleSidebar);
    
    // New chat buttons
    newChatBtn.addEventListener('click', startNewChat);
    newChatBtnSidebar.addEventListener('click', startNewChat);
    
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
}

// Authentication handlers
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const loginBtn = document.getElementById('loginBtn');
    
    loginBtn.disabled = true;
    loginBtn.innerHTML = '<span>Logging in...</span>';
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        
        const data = await response.json();
        
        if (data.authenticated) {
            currentUser = data.user;
            showMainInterface();
            await loadChatSessions();
            showNotification('Login successful!', 'success');
        } else {
            showNotification(data.error || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('Network error. Please try again.', 'error');
    } finally {
        loginBtn.disabled = false;
        loginBtn.innerHTML = '<span>Login</span>';
    }
}

async function handleLogout() {
    try {
        await fetch('/api/logout', { method: 'POST' });
        currentUser = null;
        currentSessionId = null;
        chatHistory = [];
        showLoginInterface();
        showNotification('Logged out successfully', 'success');
    } catch (error) {
        console.error('Logout error:', error);
    }
}

// Chat session management
async function loadChatSessions() {
    try {
        const response = await fetch('/api/chat/sessions');
        const data = await response.json();
        
        if (data.success) {
            renderChatSessions(data.sessions);
        }
    } catch (error) {
        console.error('Failed to load chat sessions:', error);
    }
}

function renderChatSessions(sessions) {
    chatSessions.innerHTML = '';
    
    sessions.forEach(session => {
        const sessionElement = document.createElement('div');
        sessionElement.className = 'chat-session-item';
        sessionElement.setAttribute('data-session-id', session.id);
        
        if (session.id === currentSessionId) {
            sessionElement.classList.add('active');
        }
        
        sessionElement.innerHTML = `
            <div class="session-info">
                <div class="session-title">${session.title}</div>
                <div class="session-time">${formatTime(session.created_at)}</div>
            </div>
            <div class="session-actions">
                <button class="session-action" onclick="deleteSession('${session.id}')">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        
        sessionElement.addEventListener('click', () => loadChatSession(session.id));
        chatSessions.appendChild(sessionElement);
    });
}

async function startNewChat() {
    try {
        const response = await fetch('/api/chat/sessions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title: 'New Chat' }),
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentSessionId = data.session_id;
            chatHistory = [];
            clearChat();
            showWelcomeScreen();
            await loadChatSessions();
        }
    } catch (error) {
        console.error('Failed to create new chat:', error);
    }
}

async function loadChatSession(sessionId) {
    try {
        const response = await fetch(`/api/chat/sessions/${sessionId}/history`);
        const data = await response.json();
        
        if (data.success) {
            currentSessionId = sessionId;
            chatHistory = data.messages;
            renderChatHistory();
            showChatInterface();
            
            // Update active session in sidebar
            document.querySelectorAll('.chat-session-item').forEach(item => {
                item.classList.remove('active');
            });
            document.querySelector(`[data-session-id="${sessionId}"]`).classList.add('active');
        }
    } catch (error) {
        console.error('Failed to load chat session:', error);
    }
}

async function deleteSession(sessionId) {
    if (confirm('Are you sure you want to delete this chat?')) {
        try {
            const response = await fetch(`/api/chat/sessions/${sessionId}`, {
                method: 'DELETE',
            });
            
            const data = await response.json();
            
            if (data.success) {
                await loadChatSessions();
                
                if (sessionId === currentSessionId) {
                    currentSessionId = null;
                    chatHistory = [];
                    showWelcomeScreen();
                }
                
                showNotification('Chat deleted', 'success');
            }
        } catch (error) {
            console.error('Failed to delete session:', error);
        }
    }
}

// UI State Management
function showWelcomeScreen() {
    copilotWelcome.classList.remove('hidden');
    chatInterface.classList.add('hidden');
    isFirstMessage = true;
}

function showChatInterface() {
    copilotWelcome.classList.add('hidden');
    chatInterface.classList.remove('hidden');
    isFirstMessage = false;
    
    // Scroll to bottom
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

function clearChat() {
    chatMessages.innerHTML = '';
    centerInputField.value = '';
    chatInputField.value = '';
    centerSendBtn.disabled = true;
    chatSendBtn.disabled = true;
}

function renderChatHistory() {
    chatMessages.innerHTML = '';
    
    chatHistory.forEach(message => {
        addMessageToChat(message.content, message.type, false);
    });
}

// Sidebar toggle for mobile
function toggleSidebar() {
    sidebar.classList.toggle('open');
}

// Message handling
function setupSuggestions() {
    document.querySelectorAll('.suggestion-item').forEach(item => {
        item.addEventListener('click', () => {
            const text = item.getAttribute('data-text');
            centerInputField.value = text;
            centerSendBtn.disabled = false;
            sendMessageFromCenter();
        });
    });
}

async function sendMessageFromCenter() {
    const message = centerInputField.value.trim();
    if (!message) return;
    
    if (!currentSessionId) {
        await startNewChat();
    }
    
    centerInputField.value = '';
    centerSendBtn.disabled = true;
    
    showChatInterface();
    addMessageToChat(message, 'user');
    
    await sendMessageToAPI(message);
}

async function sendMessageFromChat() {
    const message = chatInputField.value.trim();
    if (!message) return;
    
    if (!currentSessionId) {
        await startNewChat();
    }
    
    chatInputField.value = '';
    chatSendBtn.disabled = true;
    
    addMessageToChat(message, 'user');
    
    await sendMessageToAPI(message);
}

async function sendMessageToAPI(message) {
    if (isTyping) return;
    
    isTyping = true;
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: currentSessionId,
            }),
        });
        
        const data = await response.json();
        
        hideTypingIndicator();
        
        if (response.ok) {
            addMessageToChat(data.response, 'assistant');
            
            // Update chat sessions to reflect new activity
            await loadChatSessions();
        } else {
            addMessageToChat('Sorry, I encountered an error. Please try again.', 'assistant');
        }
    } catch (error) {
        console.error('API Error:', error);
        hideTypingIndicator();
        addMessageToChat('Network error. Please check your connection and try again.', 'assistant');
    } finally {
        isTyping = false;
    }
}

function addMessageToChat(content, type, scroll = true) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = type === 'user' ? 'U' : '<i class="fas fa-brain"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (type === 'assistant') {
        // Use marked to parse markdown
        messageContent.innerHTML = marked.parse(content);
        
        // Wrap tables for better scrolling
        const tables = messageContent.querySelectorAll('table');
        tables.forEach(table => {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-container';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        });
    } else {
        messageContent.textContent = content;
    }
    
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = formatTime(new Date());
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    messageContent.appendChild(timestamp);
    
    chatMessages.appendChild(messageDiv);
    
    if (scroll) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant typing-indicator';
    typingDiv.id = 'typing-indicator';
    
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-brain"></i>
        </div>
        <div class="message-content">
            <div class="loading-dots">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// Utility functions
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

function formatTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    
    return date.toLocaleDateString();
}

function showNotification(message, type = 'info') {
    notificationText.textContent = message;
    notification.classList.add('show');
    notification.classList.remove('success', 'error', 'info');
    notification.classList.add(type);
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Auto-login for default user (development convenience)
document.addEventListener('DOMContentLoaded', () => {
    // Auto-fill and attempt login for the default user
    setTimeout(async () => {
        if (loginContainer && !loginContainer.classList.contains('hidden')) {
            document.getElementById('username').value = 'admin01';
            document.getElementById('password').value = '123456';
            
            // Auto-submit login form
            loginForm.dispatchEvent(new Event('submit'));
        }
    }, 500);
});
