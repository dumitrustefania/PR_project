import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './index.css';
import UserList from './components/UserList';
import UserDetails from './components/UserDetails';
import Statistics from './components/Statistics';

function App() {
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
            </div>
        </Router>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));
