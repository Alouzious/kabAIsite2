const config = {
  // API Endpoints
  API_BASE_URL: process.env.REACT_APP_API_BASE_URL || '/api',
  MEDIA_URL: process.env.REACT_APP_MEDIA_URL || '/media',
  
  // Site Information
  SITE_NAME: process.env.REACT_APP_SITE_NAME || 'KUAI Club',
  SITE_DESCRIPTION: process.env.REACT_APP_SITE_DESCRIPTION || '',
  SITE_KEYWORDS: process.env.REACT_APP_SITE_KEYWORDS || '',
  SITE_URL: process.env.REACT_APP_SITE_URL || 'http://localhost:3000',
};

export default config;
