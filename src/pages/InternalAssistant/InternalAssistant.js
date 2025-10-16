import React from 'react';
import { useLocation } from 'react-router-dom';
import EnergyAssistant from '../../components/EnergyAssistant';
import Finance from '../../components/Finance';

function InternalAssistantPage() {
  const location = useLocation();
  
  const renderContent = () => {
    if (location.pathname === '/internal_assistant/finance') return <Finance />;
    return <EnergyAssistant />;
  };

  return (
    <div>
      {renderContent()}
    </div>
  );
}

export default InternalAssistantPage;