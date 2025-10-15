import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { SnackbarProvider } from 'notistack';

import { lightTheme } from './theme';
import AppRoutes from './AppRoutes';
import { ErrorBoundary, Notifications } from './components/shared';
import { queryClient } from './lib/queryClient';

function App() {
  return (
    <Router>
      <div className="app">
        <header className="header">
          <img src={logo} alt="Logo" />
          <nav className="header-nav">
            <Link to="/internal_assistant">Internal Assistant</Link>
            <Link to="/external_assistant">External assistant</Link>
            <Link to="/data_insights">Data Insights</Link>
          </nav>
        </header>
        <Routes>
          <Route path="/" element={<InternalAssistant />} />
          <Route path="/internal_assistant" element={<InternalAssistant />} />
          <Route path="/internal_assistant/energy" element={<InternalAssistant />} />
          <Route path="/internal_assistant/finance" element={<InternalAssistant />} />
          <Route path="/external_assistant" element={<ExternalAssistant />} />
          <Route path="/data_insights" element={<DataInsights />} />
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