import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { SnackbarProvider } from 'notistack';

import { lightTheme } from './theme';
import AppRoutes from './AppRoutes';
import { ErrorBoundary, Notifications } from './components/shared';

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider theme={lightTheme}>
        <CssBaseline />
        <SnackbarProvider maxSnack={3}>
          <Router>
            <AppRoutes />
            <Notifications />
          </Router>
        </SnackbarProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;