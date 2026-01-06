import React from 'react';
import { Link } from 'react-router-dom';
import './IndabaxFooter.css';

const IndabaxFooter = ({ siteSettings = {}, contactInfo = {} }) => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="indabax-footer">
      <div className="container">
        <div className="row">
          {/* About Column */}
          <div className="col-lg-4 col-md-6 mb-4">
            <h5 className="footer-heading">About Indabax Kabale</h5>
            <p className="footer-text">
              Indabax Kabale is part of the Deep Learning Indaba network, 
              bringing world-class AI education and networking opportunities 
              to Uganda. Join us in shaping the future of AI in Africa.
            </p>
            <div className="social-links mt-3">
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
              {siteSettings. instagram_url && (
                <a href={siteSettings.instagram_url} target="_blank" rel="noopener noreferrer">
                  <i className="fab fa-instagram"></i>
                </a>
              )}
              {siteSettings.linkedin_url && (
                <a href={siteSettings.linkedin_url} target="_blank" rel="noopener noreferrer">
                  <i className="fab fa-linkedin-in"></i>
                </a>
              )}
            </div>
          </div>

          {/* Quick Links */}
          <div className="col-lg-2 col-md-6 mb-4">
            <h5 className="footer-heading">Quick Links</h5>
            <ul className="footer-links">
              <li><a href="#about">About</a></li>
              <li><a href="#events">Events</a></li>
              <li><a href="#speakers">Speakers</a></li>
              <li><a href="#gallery">Gallery</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </div>

          {/* Resources */}
          <div className="col-lg-3 col-md-6 mb-4">
            <h5 className="footer-heading">Resources</h5>
            <ul className="footer-links">
              <li><a href="#register">Register</a></li>
              <li><a href="https://deeplearningindaba.com" target="_blank" rel="noopener noreferrer">Deep Learning Indaba</a></li>
              <li><Link to="/">KUAI Club</Link></li>
              <li><a href="#schedule">Event Schedule</a></li>
            </ul>
          </div>

          {/* Contact Info */}
          <div className="col-lg-3 col-md-6 mb-4">
            <h5 className="footer-heading">Contact Us</h5>
            <ul className="footer-contact">
              {contactInfo.email && (
                <li>
                  <i className="fas fa-envelope me-2"></i>
                  <a href={`mailto:${contactInfo.email}`}>{contactInfo.email}</a>
                </li>
              )}
              {contactInfo.phone && (
                <li>
                  <i className="fas fa-phone me-2"></i>
                  <a href={`tel:${contactInfo.phone}`}>{contactInfo.phone}</a>
                </li>
              )}
              {contactInfo.address && (
                <li>
                  <i className="fas fa-map-marker-alt me-2"></i>
                  {contactInfo.address}
                </li>
              )}
            </ul>
          </div>
        </div>

        <hr className="footer-divider" />

        {/* Bottom Bar */}
        <div className="footer-bottom">
          <div className="row align-items-center">
            <div className="col-md-6 text-center text-md-start">
              <p className="mb-0">
                © {currentYear} Indabax Kabale. All rights reserved. 
              </p>
            </div>
            <div className="col-md-6 text-center text-md-end">
              <p className="mb-0">
                Powered by <Link to="/">KUAI Club</Link> | Part of <a href="https://deeplearningindaba.com" target="_blank" rel="noopener noreferrer">Deep Learning Indaba</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default IndabaxFooter;