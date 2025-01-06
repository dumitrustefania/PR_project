import React, { useState, useEffect } from 'react';  // Add this import
import ReactDOM from 'react-dom';
import './index.css';  // Global styles for your app
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UserList from './components/UserList';
import UserDetails from './components/UserDetails';
import Statistics from './components/Statistics';
import Register from './components/Register';  // Import your Register component
import io from 'socket.io-client';  // Import socket.io-client

// Create a socket connection for the entire app
const socket = io('https://pr-project-f8c7fbee3ae5.herokuapp.com');  // Ensure this is the correct backend URL

function App() {
    const [isModalOpen, setIsModalOpen] = useState(false);  // Modal state
    const [cardId, setCardId] = useState(null);  // Card ID state

    // Listen for the 'new_user_detected' event from the backend
    useEffect(() => {
        socket.on('new_user_detected', (data) => {
            setCardId(data.card_id);
            setIsModalOpen(true);  // Open the modal when a new user is detected
        });

        // Clean up the socket listener when the component unmounts
        return () => socket.off('new_user_detected');
    }, []);

    return (
        <Router>
            <div className="app">
                <Routes>
                    <Route path="/" element={
                        <div>
                            <UserList />
                            <Statistics />
                        </div>
                    } />
                    <Route path="/user/:id" element={<UserDetails />} />
                </Routes>

                {/* Modal for registering new user */}
                {isModalOpen && (
                    <Register
                        cardId={cardId}  // Pass the cardId to the Register component
                        setIsModalOpen={setIsModalOpen}  // Function to close the modal
                    />
                )}
            </div>
        </Router>
    );
}

// Render the App component in the 'root' div
ReactDOM.render(<App />, document.getElementById('root'));
