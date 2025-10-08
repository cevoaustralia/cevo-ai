import React from 'react';
import { Link } from 'react-router-dom';

function ExternalAssistant() {
  return (
    <div className="main-container">
      <nav className="sidebar">
        <ul>
          <li><Link to="/external_assistant">External Assistant</Link></li>
        </ul>
      </nav>
      <main className="content">
        <div><h2>External Assistant Page</h2><p>Welcome to the External Assistant Page!</p></div>
      </main>
    </div>
  );
}

export default ExternalAssistant;