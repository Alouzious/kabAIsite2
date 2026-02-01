import React, { useEffect, useState } from 'react';
import axios from 'axios';
import config from "../../api/config";

const typeLabels = {
  video: 'YouTube Video',
  doc: 'Google Doc',
  slide: 'Slides',
  link: 'Other Link',
  file: 'File Upload',
};

const LearningResourcesSection = () => {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    axios.get(`${config.API_BASE_URL}/indabax/resources/`)
      .then(res => {
        console.log('API Response:', res.data);
        const data = res.data.results || res.data || [];
        console.log('Extracted resources:', data);
        setResources(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading resources:', err);
        setError('Failed to load resources.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center p-4">Loading resources...</div>;
  if (error) return <div className="alert alert-danger">{error}</div>;
  if (!resources.length) return <div className="text-center p-4">No learning resources found.</div>;

  return (
    <section className="indabax-resources">
      <div className="container">
        <h2>Learning Resources</h2>
        <div className="resources-list">
          {resources.map(res => (
            <div key={res.id} className="resource-card">
              {res.image_url && (
                <div className="resource-image">
                  <img 
                    src={res.image_url} 
                    alt={res.title}
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                </div>
              )}
              <div className="resource-content">
                <span className="resource-type">{typeLabels[res.resource_type]}</span>
                <h4>{res.title}</h4>
                <p>{res.description}</p>
                <div className="resource-links">
                  {res.url && (
                    <a href={res.url} target="_blank" rel="noopener noreferrer" className="btn btn-primary">
                      View Resource
                    </a>
                  )}
                  {res.file_url && (
                    <a href={res.file_url} target="_blank" rel="noopener noreferrer" className="btn btn-secondary">
                      Download File
                    </a>
                  )}
                </div>
                <div className="resource-meta">
                  {res.uploaded_by && <span>Uploaded by: {res.uploaded_by}</span>}
                  <span>Added: {new Date(res.date_added).toLocaleDateString()}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default LearningResourcesSection;