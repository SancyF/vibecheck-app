const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const fetchVibeData = async (location) => {
  const response = await fetch(`${API_BASE}/api/vibe/${encodeURIComponent(location)}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

export const fetchPopularLocations = async () => {
  const response = await fetch(`${API_BASE}/api/locations`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};