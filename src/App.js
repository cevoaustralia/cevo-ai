import React from 'react';
import './App.css';
import logo from './logo.png';

function App() {
  return (
    <div className="app">
      <header className="header">
        <img src={logo} alt="Logo" />
      </header>
      <div className="main-container">
        <nav className="sidebar">
          <ul>
            <li><a href="#home">Home</a></li>
          </ul>
        </nav>
        <main className="content">
          <h2>Home Page</h2>
          <p>Welcome to the home page!</p>
        </main>
      </div>
    </div>
  );
}

export default App;