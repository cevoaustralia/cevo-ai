import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import logo from './logo.png';
import Home from './pages/Home';
import Blog from './pages/Blog';
import Contact from './pages/Contact';

function App() {
  return (
    <Router>
      <div className="app">
        <header className="header">
          <img src={logo} alt="Logo" />
          <nav className="header-nav">
            <Link to="/">Home</Link>
            <Link to="/blog">Blog</Link>
            <Link to="/contact">Contact Us</Link>
          </nav>
        </header>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/energy" element={<Home />} />
          <Route path="/mortgage" element={<Home />} />
          <Route path="/blog" element={<div className="content"><Blog /></div>} />
          <Route path="/contact" element={<div className="content"><Contact /></div>} />
        </Routes>
        <footer className="footer">
          Contact Us
        </footer>
      </div>
    </Router>
  );
}

export default App;