import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './IndabaxAbout.css';
import config from "../../api/config";

const IndabaxAboutSection = () => {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${config.API_BASE_URL}/indabax/settings/current/`)
      .then(res => {
        setSettings(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load settings.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="about-loading">Loading...</div>;
  if (error) return <div className="about-error">{error}</div>;
  if (!settings) return null;

  const hasVisionMission = settings.vision_description || settings.mission_description;

  return (
    <section className="indabax-about">
      {/* About Section */}
      <div className="about-container">
        <div className="about-content">
          <div className="about-text">
            <h2 className="about-title">{settings.about_title}</h2>
            <div className="about-divider"></div>
            <p className="about-description">{settings.about_description}</p>
          </div>
          
          {settings.about_image_url && (
            <div className="about-image-wrapper">
              <img 
                src={settings.about_image_url} 
                alt={settings.about_title} 
                className="about-image"
              />
              <div className="about-image-overlay"></div>
            </div>
          )}
        </div>
      </div>

      {/* Vision & Mission Section */}
      {hasVisionMission && (
        <div className="vision-mission-section">
          <div className="vm-container">
            {settings.vision_mission_image_url && (
              <div className="vm-image-wrapper">
                <img 
                  src={settings.vision_mission_image_url} 
                  alt="Vision and Mission" 
                  className="vm-image"
                />
              </div>
            )}

            <div className="vm-content">
              {settings.vision_description && (
                <div className="vm-card vision-card">
                  <div className="vm-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                  </div>
                  <h3 className="vm-title">{settings.vision_title || 'Our Vision'}</h3>
                  <p className="vm-description">{settings.vision_description}</p>
                </div>
              )}

              {settings.mission_description && (
                <div className="vm-card mission-card">
                  <div className="vm-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                      <path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>
                    </svg>
                  </div>
                  <h3 className="vm-title">{settings.mission_title || 'Our Mission'}</h3>
                  <p className="vm-description">{settings.mission_description}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default IndabaxAboutSection;