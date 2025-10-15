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
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={lightTheme}>
          <CssBaseline />
          <SnackbarProvider maxSnack={3}>
            <Router>
              <AppRoutes />
              <Notifications />
            </Router>
          </SnackbarProvider>
        </ThemeProvider>
        <ReactQueryDevtools initialIsOpen={false} />
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;