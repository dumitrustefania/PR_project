import './Register.css';  // Import the CSS file for the modal styling

function Register({ cardId, setIsModalOpen }) {
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
            {cardId && (
                <div className="modal-overlay">
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
                </div>
            )}
        </div>
    );
}

export default Register;
