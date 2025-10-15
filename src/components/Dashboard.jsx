import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
} from '@mui/material';
import {
  ElectricBolt,
  TrendingUp,
  Assessment,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();

  const cards = [
    {
      title: 'Energy Assistant',
      description: 'Chat with our AI assistant for energy queries',
      icon: <ElectricBolt sx={{ fontSize: 40, color: 'primary.main' }} />,
      action: () => navigate('/energy'),
    },
    {
      title: 'Analytics',
      description: 'View energy usage analytics and insights',
      icon: <Assessment sx={{ fontSize: 40, color: 'secondary.main' }} />,
      action: () => navigate('/analytics'),
    },
    {
      title: 'Performance',
      description: 'Monitor system performance metrics',
      icon: <TrendingUp sx={{ fontSize: 40, color: 'success.main' }} />,
      action: () => navigate('/analytics'),
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Welcome to Cevo AI
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Your intelligent energy management platform
      </Typography>

      <Grid container spacing={3}>
        {cards.map((card, index) => (
          <Grid item xs={12} md={4} key={index}>
            <Card sx={{ height: '100%', cursor: 'pointer' }} onClick={card.action}>
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Box sx={{ mb: 2 }}>
                  {card.icon}
                </Box>
                <Typography variant="h6" gutterBottom>
                  {card.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {card.description}
                </Typography>
                <Button variant="outlined" size="small">
                  Get Started
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Dashboard;