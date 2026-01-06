import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './IndabaxNavbar.css';

const IndabaxNavbar = ({ siteSettings = {} }) => {
  const location = useLocation();
  const [scrolled, setScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Handle scroll effect
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsMobileMenuOpen(false);
  };

  const isActive = (path) => location.pathname === path;

  return (
    <>
      {/* Top Bar */}
      <div className="indabax-top-bar">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-md-6 text-start">
              <span className="indabax-tagline">
                <i className="fas fa-calendar-alt me-2"></i>
                Indabax Kabale 2025 - AI for Everyone
              </span>
            </div>
            <div className="col-md-6 d-flex justify-content-end align-items-center gap-3">
              {/* Social Media Links */}
              <div className="social-links d-flex gap-2">
                {siteSettings.facebook_url && (
                  <a href={siteSettings.facebook_url} target="_blank" rel="noopener noreferrer">
                    <i className="fab fa-facebook-f"></i>
                  </a>
                )}
                {siteSettings.twitter_url && (
                  <a href={siteSettings.twitter_url} target="_blank" rel="noopener noreferrer">
                    <i className="fab fa-twitter"></i>
                  </a>
                )}
                {siteSettings.instagram_url && (
                  <a href={siteSettings.instagram_url} target="_blank" rel="noopener noreferrer">
                    <i className="fab fa-instagram"></i>
                  </a>
                )}
              </div>
              {/* Back to Main Site */}
              <Link to="/" className="btn btn-sm btn-outline-light">
                <i className="fas fa-arrow-left me-1"></i> Back to KUAI
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Main Navbar */}
      <nav className={`indabax-navbar navbar navbar-expand-lg sticky-top ${scrolled ? 'scrolled' : ''}`}>
        <div className="container">
          {/* Logo */}
          <Link className="navbar-brand" to="/communities/indabax">
            <img 
              src={siteSettings.indabax_logo || '/logo192.png'} 
              alt="Indabax Kabale" 
              height="40"
            />
            <span className="brand-text ms-2">Indabax Kabale</span>
          </Link>

          {/* Mobile Toggle */}
          <button 
            className="navbar-toggler" 
            type="button" 
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          {/* Navigation Links */}
          <div className={`collapse navbar-collapse ${isMobileMenuOpen ? 'show' : ''}`}>
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <a 
                  href="#home" 
                  className="nav-link"
                  onClick={(e) => {
                    e.preventDefault();
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                    setIsMobileMenuOpen(false);
                  }}
                >
                  Home
                </a>
              </li>
              <li className="nav-item">
                <a 
                  href="#about" 
                  className="nav-link"
                  onClick={(e) => {
                    e. preventDefault();
                    scrollToSection('indabax-about');
                  }}
                >
                  About
                </a>
              </li>
              <li className="nav-item">
                <a 
                  href="#events" 
                  className="nav-link"
                  onClick={(e) => {
                    e.preventDefault();
                    scrollToSection('indabax-events');
                  }}
                >
                  Events
                </a>
              </li>
              <li className="nav-item">
                <a 
                  href="#speakers" 
                  className="nav-link"
                  onClick={(e) => {
                    e.preventDefault();
                    scrollToSection('indabax-speakers');
                  }}
                >
                  Speakers
                </a>
              </li>
              <li className="nav-item">
                <a 
                  href="#gallery" 
                  className="nav-link"
                  onClick={(e) => {
                    e.preventDefault();
                    scrollToSection('indabax-gallery');
                  }}
                >
                  Gallery
                </a>
              </li>
              <li className="nav-item">
                <a 
                  href="#contact" 
                  className="nav-link"
                  onClick={(e) => {
                    e.preventDefault();
                    scrollToSection('indabax-contact');
                  }}
                >
                  Contact
                </a>
              </li>
              <li className="nav-item">
                <a href="#register" className="btn btn-primary ms-2">
                  Register Now
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
};

export default IndabaxNavbar;