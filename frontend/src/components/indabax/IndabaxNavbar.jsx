import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import './IndabaxNavbar.css';


const IndabaxNavbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  // Helper to navigate to home and scroll to section
  const goToHomeSection = (sectionId) => {
    setIsOpen(false);
    if (location.pathname === '/') {
      // Already on home, just scroll
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      // Navigate to home with hash, then scroll
      navigate('/');
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 400);
    }
  };

  return (
    <nav className="indabax-navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <Link to="/indabax">
            <span className="brand-text">IndabaX Kabale</span>
          </Link>
        </div>

        {/* Mobile Menu Toggle */}
        <button className="navbar-toggle" onClick={toggleMenu}>
          <span className="bar"></span>
          <span className="bar"></span>
          <span className="bar"></span>
        </button>

        {/* Navigation Links */}
        <ul className={`navbar-menu ${isOpen ? 'active' : ''}`}>
          <li>
            <a href="#hero" onClick={() => setIsOpen(false)}>Home</a>
          </li>
          <li>
            <a href="#about" onClick={() => setIsOpen(false)}>About</a>
          </li>
          <li>
            <a href="#leaders" onClick={() => setIsOpen(false)}>Leaders</a>
          </li>
          <li>
            <a href="#gallery" onClick={() => setIsOpen(false)}>Gallery</a>
          </li>
          <li>
            <a href="#resources" onClick={() => setIsOpen(false)}>Resources</a>
          </li>
          <li>
            <a href="#contact" onClick={() => setIsOpen(false)}>Contact</a>
          </li>
          <li>
            <a href="#community" onClick={(e) => { e.preventDefault(); goToHomeSection('community'); }}>KabAIClub</a>
          </li>
          <li>
            <a href="#event-section" onClick={(e) => { e.preventDefault(); goToHomeSection('event-section'); }}>Events</a>
          </li>
          <li>
            <a href="#news-section" onClick={(e) => { e.preventDefault(); goToHomeSection('news-section'); }}>News</a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default IndabaxNavbar;