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
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add assistant response
        addMessage(data.response || 'Sorry, I couldn\'t process that request.', 'assistant');
        
        // Update chat history
        chatHistory.push({
            user: message,
            response: data.response,
            follow_up: data.follow_up
        });

        if (data.follow_up) {
            showNotification(`Follow-up: ${data.follow_up}`);
        }

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
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (sender === 'assistant') {
        // Parse markdown for assistant messages
        messageContent.innerHTML = marked.parse(content);
    } else {
        messageContent.textContent = content;
    }
    
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    
    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(timestamp);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTypingIndicator() {
    const typingId = `typing-${Date.now()}`;
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = typingId;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const loadingDots = document.createElement('div');
    loadingDots.className = 'loading-dots';
    loadingDots.innerHTML = '<div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div>';
    
    messageContent.appendChild(loadingDots);
    messageDiv.appendChild(messageContent);
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
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                </div>
            `;
            
            chatMessages.appendChild(typingDiv);
            scrollToBottom();
        }

        function hideTypingIndicator() {
            isTyping = false;
            const typingIndicator = document.getElementById('typingIndicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
        }

        function handleBotResponse(userMessage) {
            // This is where you'd integrate with your actual API
            // For now, we'll simulate different types of responses
            
            const lowerMessage = userMessage.toLowerCase();
            
            if (lowerMessage.includes('table') || lowerMessage.includes('database')) {
                const tableResponse = `
                    <p>Here are the tables in your database:</p>
                    <table>
                        <tr><th>Table Name</th><th>Records</th><th>Last Modified</th></tr>
                        <tr><td>users</td><td>1,234</td><td>2024-01-15</td></tr>
                        <tr><td>products</td><td>856</td><td>2024-01-14</td></tr>
                        <tr><td>orders</td><td>2,891</td><td>2024-01-15</td></tr>
                        <tr><td>customers</td><td>1,045</td><td>2024-01-13</td></tr>
                    </table>
                `;
                addMessage(tableResponse, 'bot', true);
                updateSuggestions(['Show me user details', 'Analyze product performance', 'Recent orders summary']);
            } else if (lowerMessage.includes('sales') || lowerMessage.includes('top')) {
                const salesResponse = `
                    <p>Here are the top 10 records by sales:</p>
                    <table>
                        <tr><th>Product</th><th>Sales</th><th>Revenue</th></tr>
                        <tr><td>Laptop Pro</td><td>145</td><td>$145,000</td></tr>
                        <tr><td>Smartphone X</td><td>289</td><td>$134,500</td></tr>
                        <tr><td>Tablet Ultra</td><td>167</td><td>$89,350</td></tr>
                        <tr><td>Headphones Max</td><td>234</td><td>$78,900</td></tr>
                        <tr><td>Monitor 4K</td><td>98</td><td>$65,340</td></tr>
                    </table>
                `;
                addMessage(salesResponse, 'bot', true);
                updateSuggestions(['Show monthly trends', 'Compare with last year', 'Product category analysis']);
            } else if (lowerMessage.includes('query') || lowerMessage.includes('sql')) {
                const queryResponse = `
                    <p>I can help you build SQL queries! Here's an example of a complex query:</p>
                    <pre>SELECT 
    p.product_name,
    SUM(o.quantity) as total_sold,
    SUM(o.quantity * p.price) as revenue,
    AVG(r.rating) as avg_rating
FROM products p
JOIN orders o ON p.id = o.product_id
LEFT JOIN reviews r ON p.id = r.product_id
WHERE o.order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY p.id, p.product_name
HAVING total_sold > 10
ORDER BY revenue DESC
LIMIT 10;</pre>
                    <p>This query shows top-selling products in the last 30 days with their ratings. What specific query do you need help with?</p>
                `;
                addMessage(queryResponse, 'bot', true);
                updateSuggestions(['Explain this query', 'Optimize query performance', 'Add filters to query']);
            } else {
                const defaultResponse = `I understand you're asking about: "${userMessage}". I'm here to help you with database queries, data analysis, and insights. Could you be more specific about what you'd like to explore?`;
                addMessage(defaultResponse, 'bot');
                updateSuggestions(['Show database schema', 'Run a sample query', 'Explain data relationships']);
            }
        }

        function updateSuggestions(suggestionsList) {
            suggestions.innerHTML = '';
            suggestionsList.forEach(suggestion => {
                const suggestionBtn = document.createElement('button');
                suggestionBtn.className = 'suggestion';
                suggestionBtn.textContent = suggestion;
                suggestionBtn.addEventListener('click', () => {
                    inputField.value = suggestion;
                    sendBtn.disabled = false;
                    sendMessage();
                });
                suggestions.appendChild(suggestionBtn);
            });
        }

        function showNotification(message) {
            notificationText.textContent = message;
            notification.classList.add('show');
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }

        // Initialize
        updateSuggestions(['Show me all tables', 'Top performing products', 'Recent activity summary']);
        
        // Add scroll to top button
        addScrollToTopButton();
        
        // Add keyboard shortcut for scroll to top (Ctrl + Home)
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Home') {
                e.preventDefault();
                scrollToTop();
            }
            // Scroll to bottom (Ctrl + End)
            if (e.ctrlKey && e.key === 'End') {
                e.preventDefault();
                scrollToBottom();
            }
        });