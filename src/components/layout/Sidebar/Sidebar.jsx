import React, { useState } from 'react';
import {
  Box,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Divider,
  Collapse,
} from '@mui/material';
import {
  Dashboard,
  Assessment,
  Settings,
  ElectricBolt,
  AccountBalance,
  ExpandLess,
  ExpandMore,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const menuItems = [
  { text: 'Dashboard', icon: <Dashboard />, path: '/' },
  { 
    text: 'Internal Assistant', 
    icon: <Assessment />, 
    path: '/internal_assistant',
    subItems: [
      { text: 'Energy', icon: <ElectricBolt />, path: '/internal_assistant/energy' },
      { text: 'Finance', icon: <AccountBalance />, path: '/internal_assistant/finance' },
    ]
  },
  { text: 'External Assistant', icon: <Assessment />, path: '/external_assistant' },
  { text: 'Data Insights', icon: <Assessment />, path: '/data_insights' },
  { text: 'Settings', icon: <Settings />, path: '/settings' },
];

const Sidebar = ({ collapsed }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [openItems, setOpenItems] = useState({});

  const handleItemClick = (item) => {
    if (item.subItems) {
      setOpenItems(prev => ({
        ...prev,
        [item.text]: !prev[item.text]
      }));
    } else {
      navigate(item.path);
    }
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Toolbar>
        <Typography variant="h6" noWrap sx={{ display: collapsed ? 'none' : 'block' }}>
          Cevo AI
        </Typography>
      </Toolbar>
      <Divider />
      <List sx={{ flexGrow: 1 }}>
        {menuItems.map((item) => (
          <React.Fragment key={item.text}>
            <ListItem disablePadding>
              <ListItemButton
                selected={location.pathname === item.path}
                onClick={() => handleItemClick(item)}
                sx={{
                  minHeight: 48,
                  justifyContent: collapsed ? 'center' : 'initial',
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: collapsed ? 'auto' : 3,
                    justifyContent: 'center',
                  }}
                >
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.text}
                  sx={{ opacity: collapsed ? 0 : 1 }}
                />
                {item.subItems && !collapsed && (
                  openItems[item.text] ? <ExpandLess /> : <ExpandMore />
                )}
              </ListItemButton>
            </ListItem>
            {item.subItems && (
              <Collapse in={openItems[item.text] && !collapsed} timeout="auto" unmountOnExit>
                <List component="div" disablePadding>
                  {item.subItems.map((subItem) => (
                    <ListItem key={subItem.text} disablePadding>
                      <ListItemButton
                        selected={location.pathname === subItem.path}
                        onClick={() => navigate(subItem.path)}
                        sx={{ pl: 4 }}
                      >
                        <ListItemIcon sx={{ minWidth: 0, mr: 3 }}>
                          {subItem.icon}
                        </ListItemIcon>
                        <ListItemText primary={subItem.text} />
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              </Collapse>
            )}
          </React.Fragment>
        ))}
      </List>
    </Box>
  );
};

export default Sidebar;