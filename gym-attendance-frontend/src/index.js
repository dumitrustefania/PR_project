import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './index.css';
import UserList from './components/UserList';
import UserDetails from './components/UserDetails';
import Statistics from './components/Statistics';
import Register from './components/Register';  // Import your Register component
import io from 'socket.io-client';  // Import socket.io-client

// Create a socket connection for the entire app
const socket = io('https://pr-project-f8c7fbee3ae5.herokuapp.com');  // Ensure this is the correct backend URL

function App() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [cardId, setCardId] = useState(null);

    useEffect(() => {
        // Listen for the 'new_user_detected' event from the backend
        socket.on('new_user_detected', (data) => {
            setCardId(data.card_id);
            setIsModalOpen(true);  // Open the modal to register the user
        });
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

ReactDOM.render(<App />, document.getElementById('root'));
