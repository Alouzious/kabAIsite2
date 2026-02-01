import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './PartnersSection.css';
import config from "../../api/config";

const PartnersSection = () => {
  const [partners, setPartners] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const sectionRef = useRef(null);
  const cardsRef = useRef([]);

  useEffect(() => {
    axios.get(`${config.API_BASE_URL}/partners/`)
      .then(res => {
        const data = res.data.results || res.data || [];
        // Ensure data is an array before filtering
        const dataArray = Array.isArray(data) ? data : [];
        const activePartners = dataArray.filter(partner => partner.is_active);
        setPartners(activePartners);
        setLoading(false);
      })
      .catch(err => {
        console.error('ERROR loading partners:', err);
        setError('Failed to load partners.');
        setPartners([]);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const animateCards = () => {
      cardsRef.current.forEach((card, index) => {
        if (card) {
          setTimeout(() => {
            card.classList.add('animate');
          }, index * 150);
        }
      });
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCards();
          observer.disconnect();
        }
      });
    }, observerOptions);

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => observer.disconnect();
  }, [partners]);

  if (loading) {
    return (
      <section id="partners" className="partners-section">
        <div className="container">
          <div className="partners-loading">
            <div className="partners-spinner"></div>
            <p>Loading partners...</p>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section id="partners" className="partners-section">
        <div className="container">
          <div className="alert alert-danger">{error}</div>
        </div>
      </section>
    );
  }

  return (
    <section id="partners" className="partners-section" ref={sectionRef}>
      <div className="container">
        <h2 className="partners-title">Our Partners</h2>
        <div className="partners-grid">
          {partners.length === 0 ? (
            <div className="partners-no-data">
              <p>No partners available at the moment.</p>
            </div>
          ) : (
            partners.map((partner, index) => (
              <div key={partner.id} className="partner-card fade-in-up" ref={el => cardsRef.current[index] = el}>
                {partner.logo_url && (
                  <a href={partner.website_url || '#'} target="_blank" rel="noopener noreferrer" className="partner-image-link">
                    <img 
                      src={partner.logo_url} 
                      className="partner-image" 
                      alt={partner.name} 
                      loading="lazy"
                    />
                  </a>
                )}
                <div className="partner-card-body">
                  <h6 className="partner-card-title">{partner.name}</h6>
                  {partner.partnership_level && (
                    <span className="partner-type">{partner.partnership_level}</span>
                  )}
                  {partner.description && (
                    <p className="partner-card-text">
                      {partner.description.split(' ').slice(0, 20).join(' ')}
                      {partner.description.split(' ').length > 20 ? '...' : ''}
                    </p>
                  )}
                  {partner.website_url && (
                    <a href={partner.website_url} target="_blank" rel="noopener noreferrer" className="partner-website-link">
                      <span>Visit Website</span>
                      <i className="fas fa-external-link-alt"></i>
                    </a>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </section>
  );
};

export default PartnersSection;