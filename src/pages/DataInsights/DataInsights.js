import React from 'react';
import { Link } from 'react-router-dom';

function DataInsights() {
  return (
    <div className="main-container">
      <nav className="sidebar">
        <ul>
          <li><Link to="/data_insights">Data Insights</Link></li>
        </ul>
      </nav>
      <main className="content">
        <div><h2>Data Insights Page</h2><p>Welcome to the Data Insights Page!</p></div>
      </main>
    </div>
  );
}

export default DataInsights;