import React, { useState } from 'react';
import './ChatComponent.css'; // Importing CSS file for styling


const ChatComponent = () => {
    const [userInput, setUserInput] = useState('');
    const [chatResponse, setChatResponse] = useState([]);

    const handleInputChange = (e) => {
        setUserInput(e.target.value);
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
            setChatResponse(prev => [...prev, { type: 'user', text: userInput }, { type: 'bot', text: data.response }]);
            setUserInput(''); // Clear the input field after sending
        } catch (error) {
            console.error("Error fetching chat response:", error);
        }
    };
    

    return (
        <div >
            <div className="chat-box">
                {chatResponse.map((msg, index) => (
                    <div key={index} className={`chat-message ${msg.type}`}>
                        {msg.text}
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
