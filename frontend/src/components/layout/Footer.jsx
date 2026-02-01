import React, { useState, useEffect } from 'react';
import './Footer.css';
import config from "../../api/config";

const Footer = () => {
  const [showBackToTop, setShowBackToTop] = useState(false);
  const [siteSettings, setSiteSettings] = useState({});
  const [quickLinks, setQuickLinks] = useState([]);

  // Fetch site settings and quick links directly in Footer
  useEffect(() => {
    // Fetch site settings
    fetch(`${config.API_BASE_URL}/core/site-settings/`)
      .then(res => res.json())
      .then(data => {
        console.log('Footer - Site settings response:', data);
        
        if (data.results && Array.isArray(data.results) && data.results.length > 0) {
          setSiteSettings(data.results[0]);
        } else if (Array.isArray(data) && data.length > 0) {
          setSiteSettings(data[0]);
        } else if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
          setSiteSettings(data);
        } else {
          setSiteSettings({});
        }
      })
      .catch(error => {
        console.error('Footer - Error fetching site settings:', error);
        setSiteSettings({});
      });

    // Fetch quick links separately
    fetch(`${config.API_BASE_URL}/core/quick-links/`)
      .then(res => res.json())
      .then(data => {
        console.log('Footer - Quick links response:', data);
        const links = data.results || data || [];
        // Ensure links is an array before filtering
        const activeLinks = Array.isArray(links) 
          ? links.filter(link => link.is_active).sort((a, b) => (a.order || 0) - (b.order || 0))
          : [];
        setQuickLinks(activeLinks);
      })
      .catch(error => {
        console.error('Footer - Error fetching quick links:', error);
        setQuickLinks([]);
      });
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      if (window.pageYOffset > 300) {
        setShowBackToTop(true);
      } else {
        setShowBackToTop(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToTop = (e) => {
    e.preventDefault();
    window.scrollTo({ 
      top: 0, 
      behavior: 'smooth' 
    });
  };

  return (
    <footer>   
      <div className="footer-top">     
        <h5>🤖 {siteSettings.site_name || 'KUAI Club'} – Kabale University</h5>     
        <p>{siteSettings.site_tagline || 'Empowering the next generation of AI innovators at KU.'}</p>   
      </div>    
      
      <div className="footer-columns">     
        {/* QUICK LINKS */}     
        <div className="footer-section">       
          <h6>⚡ QUICK LINKS</h6>       
          <ul>         
            {quickLinks.length > 0 ? (
              quickLinks.map((link) => (
                <li key={link.id}>
                  <a 
                    href={link.url} 
                    target={link.open_new_tab ? "_blank" : "_self"}
                    rel={link.open_new_tab ? "noopener noreferrer" : undefined}
                  >
                    {link.name}
                  </a>
                </li>
              ))
            ) : (
              <li><span className="text-muted">No links yet</span></li>
            )}
          </ul>     
        </div>      

        {/* CONTACT US */}     
        <div className="footer-section">       
          <h6>📞 CONTACT US</h6>       
          {siteSettings.address && (
            <p className="contact-item">📍 {siteSettings.address}</p>
          )}
          {siteSettings.contact_email && (
            <p className="contact-item">
              📧 <a href={`mailto:${siteSettings.contact_email}`} className="contact-link">
                {siteSettings.contact_email}
              </a>
            </p>
          )}
          {siteSettings.contact_phone && (
            <p className="contact-item">
              ☎ <a href={`tel:${siteSettings.contact_phone}`} className="contact-link">
                {siteSettings.contact_phone}
              </a>
            </p>
          )}
          {!siteSettings.address && !siteSettings.contact_email && !siteSettings.contact_phone && (
            <p className="text-muted">Loading contact info...</p>
          )}
        </div>      

        {/* FOLLOW US */}     
        <div className="footer-section">       
          <h6>🌐 FOLLOW US</h6>       
          <ul className="social-links">
            {siteSettings.facebook_url && (
              <li>
                <a href={siteSettings.facebook_url} target="_blank" rel="noopener noreferrer">
                  <i className="fab fa-facebook-f"></i> Facebook
                </a>
              </li>
            )}
            {siteSettings.twitter_url && (
              <li>
                <a href={siteSettings.twitter_url} target="_blank" rel="noopener noreferrer">
                  <i className="fab fa-twitter"></i> Twitter
                </a>
              </li>
            )}
            {siteSettings.instagram_url && (
              <li>
                <a href={siteSettings.instagram_url} target="_blank" rel="noopener noreferrer">
                  <i className="fab fa-instagram"></i> Instagram
                </a>
              </li>
            )}
            {siteSettings.linkedin_url && (
              <li>
                <a href={siteSettings.linkedin_url} target="_blank" rel="noopener noreferrer">
                  <i className="fab fa-linkedin-in"></i> LinkedIn
                </a>
              </li>
            )}
            {siteSettings.youtube_url && (
              <li>
                <a href={siteSettings.youtube_url} target="_blank" rel="noopener noreferrer">
                  <i className="fab fa-youtube"></i> YouTube
                </a>
              </li>
            )}
            {siteSettings.whatsapp_url && (
              <li>
                <a href={siteSettings.whatsapp_url} target="_blank" rel="noopener noreferrer">
                  <i className="fab fa-whatsapp"></i> WhatsApp
                </a>
              </li>
            )}
            {!siteSettings.facebook_url && !siteSettings.twitter_url && !siteSettings.instagram_url && 
             !siteSettings.linkedin_url && !siteSettings.youtube_url && !siteSettings.whatsapp_url && (
              <li><span className="text-muted">No social links yet</span></li>
            )}
          </ul>    
        </div>   
      </div>    

      {/* Footer Bottom */}   
      <div className="footer-bottom">     
        <div className="footer-divider"></div>
        <a 
          href="#" 
          className="back-to-top" 
          onClick={scrollToTop}
          style={{ opacity: showBackToTop ? '1' : '0.7' }}
        >
          <span className="back-to-top-icon">⬆</span> Back to Top
        </a>     
        <p className="copyright">© 2025 {siteSettings.site_name || 'KUAI Club'}. All rights reserved.</p>     
        <p className="designer-credit">
          Designed with <span className="heart">❤️</span> by <strong>Technical Lead</strong>
        </p>   
      </div> 
    </footer>
  );
};

export default Footer;