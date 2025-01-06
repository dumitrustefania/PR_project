import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserList.css';

export default function UserList() {
    const [users, setUsers] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetch('http://localhost:5000/api/users')
            .then((res) => res.json())
            .then((data) => setUsers(Object.entries(data)));
    }, []);

    // Calculate total users and total users with valid membership
    const totalUsers = users.length;
    const totalValidUsers = users.filter(([id, user]) => user.paidMembership).length;

    return (
        <div className="user-list">
            <h1>Gym Members</h1>
            
            {/* Displaying the total users and total valid users */}
            <div className="user-stats">
                <p>Total Users: {totalUsers}</p>
                <p>Total Users with Valid Membership: {totalValidUsers}</p>
            </div>

            <table className="user-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Membership</th>
                        <th>Attendances</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map(([id, user]) => (
                        <tr key={id} onClick={() => navigate(`/user/${id}`)}>
                            <td>{`${user.firstName} ${user.lastName}`}</td>
                            <td>{user.paidMembership ? 'Valid' : 'Invalid'}</td>
                            <td>{user.attendances.length}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
