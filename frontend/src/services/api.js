import axios from 'axios';

const API_BASE = '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchDashboardOverview = async () => {
  const response = await apiClient.get('/dashboard/overview');
  return response.data;
};

export const fetchMonthlyTrend = async () => {
  const response = await apiClient.get('/dashboard/monthly-trend');
  return response.data;
};

export const fetchCategoryPerformance = async () => {
  const response = await apiClient.get('/dashboard/categories');
  return response.data;
};

export const fetchRegionalPerformance = async () => {
  const response = await apiClient.get('/dashboard/regional');
  return response.data;
};

export const fetchTopProducts = async () => {
  const response = await apiClient.get('/dashboard/top-products');
  return response.data;
};

export const fetchRfmAnalytics = async () => {
  const response = await apiClient.get('/analytics/rfm');
  return response.data;
};

export const sendChatQuery = async (question) => {
  const response = await apiClient.post('/chat/query', { question });
  return response.data;
};
