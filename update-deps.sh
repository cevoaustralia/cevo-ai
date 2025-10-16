#!/bin/bash
echo "Updating Python dependencies..."
cd backend
pip install --upgrade pip
pip install -r requirements.txt --upgrade
echo "Python dependencies updated successfully!"