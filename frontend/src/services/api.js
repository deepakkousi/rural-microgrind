import axios from 'axios';

const API_BASE = '/api';

export const fetchHealth = async () => {
  const res = await axios.get(`${API_BASE}/health`);
  return res.data;
};

export const fetchMeterData = async (limit = 96) => {
  const res = await axios.get(`${API_BASE}/data/meter?limit=${limit}`);
  return res.data;
};

export const fetchDisaggregation = async () => {
  const res = await axios.get(`${API_BASE}/disaggregation`);
  return res.data;
};

export const fetchDrilldownEvidence = async (loadId) => {
  const res = await axios.get(`${API_BASE}/disaggregation/drilldown/${loadId}`);
  return res.data;
};

export const fetchRecommendations = async () => {
  const res = await axios.get(`${API_BASE}/recommendations`);
  return res.data;
};

export const updateRecommendationStatus = async (recId, status) => {
  const res = await axios.post(`${API_BASE}/recommendations/${recId}/status`, { status });
  return res.data;
};

export const fetchVerificationSummary = async () => {
  const res = await axios.get(`${API_BASE}/verification/summary`);
  return res.data;
};

export const fetchVerificationTimeseries = async () => {
  const res = await axios.get(`${API_BASE}/verification/timeseries`);
  return res.data;
};

export const fetchEquipmentRegistry = async () => {
  const res = await axios.get(`${API_BASE}/equipment`);
  return res.data;
};

export const fetchFreshnessStatus = async () => {
  const res = await axios.get(`${API_BASE}/quality/freshness`);
  return res.data;
};

export const fetchAnomalies = async () => {
  const res = await axios.get(`${API_BASE}/quality/anomalies`);
  return res.data;
};

export const simulateEdgeFailure = async (failureType, duration = 16, channel = "water_pump_kw") => {
  const res = await axios.post(`${API_BASE}/quality/simulate-failure`, {
    failure_type: failureType,
    duration_intervals: duration,
    affected_channel: channel
  });
  return res.data;
};
