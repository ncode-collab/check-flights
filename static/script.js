document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const flightResults = document.getElementById('flight-results');

    const addMessage = (text, sender) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.innerText = text;
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    };

    const renderFlights = (flights) => {
        flightResults.innerHTML = '';
        if (!flights || flights.length === 0) {
            flightResults.innerHTML = '<div class="empty-results">No flights found for your criteria.</div>';
            return;
        }

        flights.forEach(flight => {
            const card = document.createElement('div');
            card.classList.add('flight-card');
            
            const depTime = new Date(flight.departure_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const arrTime = new Date(flight.arrival_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            card.innerHTML = `
                <div class="flight-header">
                    <span class="airline">${flight.airline}</span>
                    <span class="price">${flight.currency} ${flight.price.toFixed(2)}</span>
                </div>
                <div class="flight-info">
                    <div class="time-box">
                        <span class="time">${depTime}</span>
                        <span class="iata">${flight.origin}</span>
                    </div>
                    <div class="duration-box">
                        <span class="duration">${flight.duration.replace('PT', '').toLowerCase()}</span>
                        <span class="stops">${flight.stops === 0 ? 'Direct' : flight.stops + ' stops'}</span>
                    </div>
                    <div class="time-box">
                        <span class="time">${arrTime}</span>
                        <span class="iata">${flight.destination}</span>
                    </div>
                </div>
            `;
            flightResults.appendChild(card);
        });
    };

    const handleSend = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        userInput.value = '';
        
        // Show typing indicator or just wait
        const loadingMsg = document.createElement('div');
        loadingMsg.classList.add('message', 'assistant');
        loadingMsg.innerText = 'Thinking...';
        chatHistory.appendChild(loadingMsg);

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            
            chatHistory.removeChild(loadingMsg);
            addMessage(data.chat_response, 'assistant');
            
            if (data.flight_data) {
                renderFlights(data.flight_data);
            }
        } catch (error) {
            chatHistory.removeChild(loadingMsg);
            addMessage('Error connecting to the server. Please try again.', 'assistant');
            console.error('Error:', error);
        }
    };

    sendButton.addEventListener('click', handleSend);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });
});
