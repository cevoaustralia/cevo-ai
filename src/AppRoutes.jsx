import React from 'react';
import { Routes, Route } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout/AppLayout';
import Dashboard from './components/Dashboard';
import EnergyAssistant from './components/EnergyAssistant/EnergyAssistant';
import InternalAssistant from './pages/InternalAssistant';
import ExternalAssistant from './pages/ExternalAssistant';
import DataInsights from './pages/DataInsights';

const AppRoutes = () => {
  return (
    <AppLayout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/energy" element={<EnergyAssistant />} />
        <Route path="/internal_assistant" element={<InternalAssistant />} />
        <Route path="/internal_assistant/energy" element={<InternalAssistant />} />
        <Route path="/internal_assistant/finance" element={<InternalAssistant />} />
        <Route path="/external_assistant" element={<ExternalAssistant />} />
        <Route path="/data_insights" element={<DataInsights />} />
        <Route path="/analytics" element={<div>Analytics Coming Soon</div>} />
        <Route path="/settings" element={<div>Settings Coming Soon</div>} />
      </Routes>
    </AppLayout>
  );
};

export default AppRoutes;