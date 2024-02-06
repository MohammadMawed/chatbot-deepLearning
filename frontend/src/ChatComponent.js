import React, { useState } from 'react';
import './ChatComponent.css';

const ChatComponent = () => {
    const [userInput, setUserInput] = useState('');
    const [chatResponse, setChatResponse] = useState([]);

    const handleInputChange = (e) => {
        setUserInput(e.target.value);
    };

    const sendFeedback = async (userInput, botResponse, feedback) => {
        const feedbackDetails = {
            userInput: userInput,  // User's original message
            botResponse: botResponse,  // Bot's response to the user input
            feedback: feedback,  // User's feedback (e.g., 'positive', 'negative')
            context: {},  // Add context if available
            timestamp: new Date().toISOString(),
            userId: '12345'  // Add userId if available
        };

        try {
            await fetch('http://127.0.0.1:5000/log_interaction', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(feedbackDetails)
            });
        } catch (error) {
            console.error("Error sending feedback:", error);
        }
    };

    const handleSendClick = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ input: userInput })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Add user's message and bot's response to chatResponse
            setChatResponse(prev => [...prev, 
                { type: 'user', text: userInput, userInput: userInput },
                { type: 'bot', text: data.response, botResponse: data.response }
            ]);

            setUserInput(''); // Clear the input field after sending
        } catch (error) {
            console.error("Error fetching chat response:", error);
        }
    };

    const handleFeedbackClick = (index, feedbackType) => {
        const userMessage = chatResponse[index];
        const botMessage = chatResponse[index + 1];
        sendFeedback(userMessage.text, botMessage.text, feedbackType);
    };

    return (
        <div className="chat-container">
            <div className="chat-box">
                {chatResponse.map((message, index) => (
                    <div key={index} className={`chat-message ${message.type}`}>
                        {message.text}
                        {message.type === 'bot' && (
                            <div className="feedback-buttons">
                                <button onClick={() => handleFeedbackClick(index - 1, 'positive')}>👍</button>
                                <button onClick={() => handleFeedbackClick(index - 1, 'negative')}>👎</button>
                            </div>
                        )}
                    </div>
                ))}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    value={userInput}
                    onChange={handleInputChange}
                    className="chat-input"
                    placeholder="Type a message..."
                />
                <button onClick={handleSendClick} className="send-button">Send</button>
            </div>
        </div>
    );
};

export default ChatComponent;
