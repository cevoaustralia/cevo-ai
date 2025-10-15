import React, { useState } from 'react';
import {
  Toolbar,
  IconButton,
  Typography,
  Box,
  Avatar,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Menu as MenuIcon,
  AccountCircle,
  Logout,
  ChevronLeft,
  ChevronRight,
} from '@mui/icons-material';

const Header = ({ onMenuClick, onSidebarToggle, sidebarCollapsed }) => {
  const [anchorEl, setAnchorEl] = useState(null);

  const handleUserMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleUserMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <Toolbar>
      <IconButton
        color="inherit"
        onClick={onMenuClick}
        sx={{ mr: 2, display: { md: 'none' } }}
      >
        <MenuIcon />
      </IconButton>

      <IconButton
        color="inherit"
        onClick={onSidebarToggle}
        sx={{ mr: 2, display: { xs: 'none', md: 'flex' } }}
      >
        {sidebarCollapsed ? <ChevronRight /> : <ChevronLeft />}
      </IconButton>

      <Typography variant="h6" noWrap sx={{ flexGrow: 1 }}>
        Cevo AI Assistant
      </Typography>

      <IconButton color="inherit" onClick={handleUserMenuOpen}>
        <Avatar sx={{ width: 32, height: 32 }}>
          <AccountCircle />
        </Avatar>
      </IconButton>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleUserMenuClose}
      >
        <MenuItem onClick={handleUserMenuClose}>
          <Logout fontSize="small" sx={{ mr: 1 }} />
          Logout
        </MenuItem>
      </Menu>
    </Toolbar>
  );
};

export default Header;