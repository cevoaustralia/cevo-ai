import React from 'react';
import { Breadcrumbs, Typography, Link } from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import { NavigateNext } from '@mui/icons-material';

const Breadcrumb = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const getBreadcrumbs = () => {
    const path = location.pathname;
    
    const breadcrumbs = [{ label: 'Cevo AI Assistant', path: '/' }];
    
    if (path.startsWith('/internal_assistant')) {
      breadcrumbs.push({ label: 'Internal Assistant', path: '/internal_assistant' });
      if (path === '/internal_assistant/energy') {
        breadcrumbs.push({ label: 'Energy', path: '/internal_assistant/energy' });
      } else if (path === '/internal_assistant/finance') {
        breadcrumbs.push({ label: 'Finance', path: '/internal_assistant/finance' });
      }
    } else if (path === '/external_assistant') {
      breadcrumbs.push({ label: 'External Assistant', path: '/external_assistant' });
    } else if (path === '/data_insights') {
      breadcrumbs.push({ label: 'Data Insights', path: '/data_insights' });
    } else if (path === '/settings') {
      breadcrumbs.push({ label: 'Settings', path: '/settings' });
    } else if (path === '/analytics') {
      breadcrumbs.push({ label: 'Analytics', path: '/analytics' });
    }
    
    return breadcrumbs;
  };

  const breadcrumbs = getBreadcrumbs();

  return (
    <Breadcrumbs separator={<NavigateNext fontSize="small" />} sx={{ mb: 2 }}>
      {breadcrumbs.map((crumb, index) => (
        index === breadcrumbs.length - 1 ? (
          <Typography key={crumb.path} color="text.primary" variant="h6">
            {crumb.label}
          </Typography>
        ) : (
          <Link
            key={crumb.path}
            color="inherit"
            onClick={() => navigate(crumb.path)}
            sx={{ cursor: 'pointer', textDecoration: 'none', '&:hover': { textDecoration: 'underline' } }}
          >
            {crumb.label}
          </Link>
        )
      ))}
    </Breadcrumbs>
  );
};

export default Breadcrumb;