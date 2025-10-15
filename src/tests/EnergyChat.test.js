import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import EnergyAssistant from '../components/EnergyAssistant/EnergyAssistant';

// Mock fetch
global.fetch = jest.fn();

describe('EnergyAssistant', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders chat interface', () => {
    render(<EnergyAssistant />);
    expect(screen.getByText('Energy Assistant')).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/customer number/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/address/i)).toBeInTheDocument();
  });

  test('sends message on button click', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Test response',
        agent_used: 'CURRENT_CUSTOMER',
        reasoning: 'Test reasoning'
      })
    });

    render(<EnergyAssistant />);
    
    const input = screen.getByPlaceholderText(/ask about your energy/i);
    const button = screen.getByText('Send');
    
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:2024/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: 'Test message',
          customer_number: null,
          address: null
        })
      });
    });
  });

  test('displays bot response', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Bot response',
        agent_used: 'NEW_CUSTOMER',
        reasoning: 'New customer query'
      })
    });

    render(<EnergyAssistant />);
    
    const input = screen.getByPlaceholderText(/ask about your energy/i);
    fireEvent.change(input, { target: { value: 'Test' } });
    fireEvent.click(screen.getByText('Send'));

    await waitFor(() => {
      expect(screen.getByText('Bot response')).toBeInTheDocument();
      expect(screen.getByText(/Agent: NEW_CUSTOMER/)).toBeInTheDocument();
    });
  });
});