import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import EnergyAssistant from '../../components/EnergyAssistant';
import MortgageAssistant from '../../components/MortgageAssistant';

function Home() {
  const location = useLocation();
  
  const renderContent = () => {
    if (location.pathname === '/energy') return <EnergyAssistant />;
    if (location.pathname === '/mortgage') return <MortgageAssistant />;
   
  };

  return (
    <div className="main-container">
      <nav className="sidebar">
        <ul>
          <li><Link to="/energy">Energy Assistant</Link></li>
          <li><Link to="/mortgage">Mortgage Assistant</Link></li>
        </ul>
      </nav>
      <main className="content">
        {renderContent()}
      </main>
    </div>
  );
}

export default Home;