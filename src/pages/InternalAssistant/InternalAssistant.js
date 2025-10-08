import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import EnergyAssistant from '../../components/EnergyAssistant';
import Finance from '../../components/Finance';

function InternalAssistantPage() {
  const location = useLocation();
  
  const renderContent = () => {
    if (location.pathname === '/internal_assistant/finance') return <Finance />;
    return <EnergyAssistant />;
  };

  return (
    <div className="main-container">
      <nav className="sidebar">
        <ul>
          <li><Link to="/internal_assistant/energy">Energy</Link></li>
          <li><Link to="/internal_assistant/finance">Finance</Link></li>
        </ul>
      </nav>
      <main className="content">
        {renderContent()}
      </main>
    </div>
  );
}

export default InternalAssistantPage;