// Chat functionality
        const chatContainer = document.getElementById('chatContainer');
        const chatMessages = document.getElementById('chatMessages');
        const welcomeScreen = document.getElementById('welcomeScreen');
        const inputField = document.getElementById('inputField');
        const sendBtn = document.getElementById('sendBtn');
        const clearBtn = document.getElementById('clearBtn');
        const suggestions = document.getElementById('suggestions');
        const notification = document.getElementById('notification');
        const notificationText = document.getElementById('notificationText');

        let chatHistory = [];
        let isTyping = false;

        // Auto-resize textarea
        inputField.addEventListener('input', () => {
            inputField.style.height = 'auto';
            inputField.style.height = inputField.scrollHeight + 'px';
            sendBtn.disabled = !inputField.value.trim();
        });

        // Send message on Enter (but not Shift+Enter)
        inputField.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Send button click
        sendBtn.addEventListener('click', sendMessage);

        // Clear chat
        clearBtn.addEventListener('click', () => {
            chatHistory = [];
            chatMessages.innerHTML = '';
            chatMessages.classList.add('hidden');
            welcomeScreen.classList.remove('hidden');
            showNotification('Chat cleared');
            updateSuggestions([]);
        });

        // Functions
        async function sendMessage() {
            const message = inputField.value.trim();
            if (!message || isTyping) return;

            // Hide welcome screen and show chat
            welcomeScreen.classList.add('hidden');
            chatMessages.classList.remove('hidden');

            // Add user message
            addMessage(message, 'user');
            
            // Clear input
            inputField.value = '';
            inputField.style.height = 'auto';
            sendBtn.disabled = true;

            // Show typing indicator
            showTypingIndicator();

            // Prepare chat history for backend as [{user, response}, ...]
            const historyForBackend = [];
            for (let i = 0; i < chatHistory.length; i += 2) {
                const userEntry = chatHistory[i];
                const botEntry = chatHistory[i + 1];
                if (userEntry && userEntry.sender === 'user') {
                    historyForBackend.push({
                        user: userEntry.content,
                        response: botEntry && botEntry.sender === 'bot' ? botEntry.content : ''
                    });
                }
            }

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        history: historyForBackend
                    })
                });
                const data = await response.json();
                hideTypingIndicator();
                addMessage(data.response, 'bot', true);
                // Optionally, store follow_up for next turn
                if (data.follow_up) {
                    chatHistory[chatHistory.length - 1].follow_up = data.follow_up;
                }
                // Optionally, update suggestions based on follow_up
                if (data.follow_up) {
                    updateSuggestions([data.follow_up]);
                } else {
                    updateSuggestions([]);
                }
            } catch (err) {
                hideTypingIndicator();
                addMessage('❌ Failed to connect to server.', 'bot');
            }
        }

        function addMessage(content, sender, isHtml = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            const avatar = document.createElement('div');
            avatar.className = `message-avatar ${sender}`;
            avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            const messageText = document.createElement('div');
            messageText.className = 'message-text';
            if (sender === 'bot') {
                messageText.innerHTML = marked.parse(content);
            } else {
                messageText.textContent = content;
            }
            // Wrap tables in .table-responsive for horizontal scroll
            messageText.querySelectorAll('table').forEach(table => {
                const wrapper = document.createElement('div');
                wrapper.className = 'table-responsive';
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            });
            messageContent.appendChild(messageText);
            // Removed message-actions (copy/like) for bot messages
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(messageContent);
            chatMessages.appendChild(messageDiv);
            
            // Smooth scroll to bottom with animation
            scrollToBottom();
            
            // Store in history
            chatHistory.push({ sender, content, timestamp: new Date() });
        }

        function scrollToBottom() {
            // Use requestAnimationFrame for smooth scrolling
            requestAnimationFrame(() => {
                chatContainer.scrollTo({
                    top: chatContainer.scrollHeight,
                    behavior: 'smooth'
                });
            });
        }

        function scrollToTop() {
            chatContainer.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }

        // Add scroll to top button functionality
        function addScrollToTopButton() {
            const scrollBtn = document.createElement('button');
            scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
            scrollBtn.className = 'scroll-to-top';
            scrollBtn.style.cssText = `
                position: fixed;
                bottom: 100px;
                right: 20px;
                width: 45px;
                height: 45px;
                border-radius: 50%;
                background: var(--primary-gradient);
                color: white;
                border: none;
                cursor: pointer;
                display: none;
                z-index: 1000;
                transition: var(--transition);
                box-shadow: var(--shadow-lg);
            `;
            scrollBtn.onclick = scrollToTop;
            document.body.appendChild(scrollBtn);

            // Show/hide scroll to top button
            chatContainer.addEventListener('scroll', () => {
                if (chatContainer.scrollTop > 300) {
                    scrollBtn.style.display = 'flex';
                    scrollBtn.style.alignItems = 'center';
                    scrollBtn.style.justifyContent = 'center';
                } else {
                    scrollBtn.style.display = 'none';
                }
            });
        }

        function showTypingIndicator() {
            isTyping = true;
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message bot';
            typingDiv.id = 'typingIndicator';
            
            typingDiv.innerHTML = `
                <div class="message-avatar bot">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="typing-indicator">
                        <div class="typing-dots">
                            <div class="typing-dot"></div>
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