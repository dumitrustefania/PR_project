import { useEffect, useState } from 'react';
import io from 'socket.io-client';

const socket = io('https://pr-project-f8c7fbee3ae5.herokuapp.com');

const Register = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [cardId, setCardId] = useState(null);

    useEffect(() => {
        // Listen for the 'new_user_detected' event from the backend
        socket.on('new_user_detected', (data) => {
            setCardId(data.card_id);
            setIsModalOpen(true);  // Open the modal to register the user
        });
    }, []);

    const handleRegisterUser = (userData) => {
        fetch('https://pr-project-f8c7fbee3ae5.herokuapp.com/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                card_id: cardId,
                data: userData,
            }),
        })
        .then((res) => res.json())
        .then((data) => {
            console.log('User registered:', data);
            setIsModalOpen(false);  // Close the modal after registration
        })
        .catch((error) => console.error('Error registering user:', error));
    };

    return (
        <div>
            {isModalOpen && (
                <div className="modal">
                    <h2>Register New User</h2>
                    <form
                        onSubmit={(e) => {
                            e.preventDefault();
                            const userData = {
                                firstName: e.target.firstName.value,
                                lastName: e.target.lastName.value,
                                paidMembership: e.target.paidMembership.checked,
                            };
                            handleRegisterUser(userData);
                        }}
                    >
                        <input type="text" name="firstName" placeholder="First Name" required />
                        <input type="text" name="lastName" placeholder="Last Name" required />
                        <label>
                            Paid Membership:
                            <input type="checkbox" name="paidMembership" />
                        </label>
                        <button type="submit">Register</button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default Register;
