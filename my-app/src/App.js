import React, { useState, useEffect } from 'react';
import axios from 'axios';
import logo from './logo.svg';
import './App.css';

function App() {
  const [newUser, setNewUser] = useState({ email: '', name: '' });
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get('http://localhost:8000/users/');
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleChange = (event) => {
    const { id, value } = event.target;
    setNewUser(prevUser => ({ ...prevUser, [id]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/users/', newUser);
      setUsers(prevUsers => [...prevUsers, response.data]);
      setNewUser({ email: '', name: '' });
    } catch (error) {
      console.error('Error creating user:', error);
    }
  };

  const handleDelete = async (userId) => {
    try {
      await axios.delete(`http://localhost:8000/users/${userId}`);
      setUsers(prevUsers => prevUsers.filter(user => user.id !== userId));
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <img src={logo} className="logo" alt="logo" />
        <span>Bem-vindo ao meu portfólio. Para começar, vamos integrar com o Google para logar.</span>
      </header>

      <form onSubmit={handleSubmit}>
        <div className="inputContainer">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            placeholder="Enter Your Email"
            value={newUser.email}

            onChange={handleChange}
          />
        </div>
        <div className="inputContainer">
          <label htmlFor="name">Nome:</label>
          <input
            type="text"
            id="name"
            placeholder="Enter Your Name"
            value={newUser.name}
            onChange={handleChange}
          />
        </div>
        <div className="inputContainer">
          <button type="submit">Submit</button>
        </div>
      </form>

      <div className="usersList">
        <h2>Users List:</h2>
        {users.length > 0 ? (
          <ul>
            {users.map(user => (
              <li key={user.id}>
                {user.id} - {user.email} - {user.name}
                <button onClick={() => handleDelete(user.id)}>Delete</button>
              </li>
            ))}
          </ul>
        ) : (
          <p>No users found.</p>
        )}
      </div>
    </div>
  );
}

export default App;
