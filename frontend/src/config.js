/**
 * API Configuration
 * Update this file to point to your deployed backend
 */

// Get API URL from environment variable or use default
export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Set to true to use sample data instead of real API (for demo mode)
export const USE_SAMPLE_DATA = false;

export const API_ENDPOINTS = {
  search: `${API_URL}/api/search`,
  feedback: `${API_URL}/api/feedback`,
  lessons: `${API_URL}/api/lessons`,
  stats: `${API_URL}/api/stats`,
  categories: `${API_URL}/api/categories`,
  regions: `${API_URL}/api/regions`,
};

export default {
  API_URL,
  USE_SAMPLE_DATA,
  API_ENDPOINTS,
};

