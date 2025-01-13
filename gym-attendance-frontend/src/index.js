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
const socket = io('https://pr-project-f8c7fbee3ae5.herokuapp.com');

function App() {
    const [isModalOpen, setIsModalOpen] = useState(false);  // Modal state
    const [cardId, setCardId] = useState(null);  // Card ID state
    const [gymClosed, setGymClosed] = useState(false);  // State to track gym status (closed or open)

    // Listen for the 'new_user_detected' event from the backend
    useEffect(() => {
        socket.on('new_user_detected', (data) => {
            setCardId(data.card_id);
            setIsModalOpen(true);  // Open the modal when a new user is detected
        });

        // Listen for the gym status update from the backend
        socket.on('gym_status_updated', (data) => {
            setGymClosed(data.gym_status);  // Update the gym status (open/closed)
        });

        // Listen for the 'user_updated' event from the server
        socket.on("user_updated", (data) => {
            console.log("User updated:", data);

            // Logic to handle the updated user data can go here
            // For now, refresh the page whenever the user is updated
            // window.location.reload();
        });

        // Clean up the socket listeners when the component unmounts
        return () => {
            socket.off('new_user_detected');
            socket.off('gym_status_updated');
            socket.off('user_updated');
        };
    }, []);

    // Function to toggle the gym status (open/closed)
    const toggleGymStatus = async () => {
        try {
            // Send a POST request to the backend to toggle the gym status
            const response = await fetch('https://pr-project-f8c7fbee3ae5.herokuapp.com/api/update_gym_status', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ gym_status: !gymClosed }), // Toggle the gym status
            });

            if (response.ok) {
                setGymClosed(!gymClosed);  // Update the local state with the new gym status
            } else {
                alert('Failed to update gym status');
            }
        } catch (error) {
            console.error('Error updating gym status:', error);
            alert('Error updating gym status');
        }
    };

    return (
        <Router>
            <div className="app">
                <h1>Gym Status: {gymClosed ? 'Closed' : 'Open'}</h1>
                <button onClick={toggleGymStatus}>
                    {gymClosed ? 'Open Gym' : 'Close Gym'}
                </button>

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
