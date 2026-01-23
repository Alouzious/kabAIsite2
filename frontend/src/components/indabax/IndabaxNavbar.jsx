import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './IndabaxNavbar.css';

const IndabaxNavbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
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
            <Link to="/communities" onClick={() => setIsOpen(false)}>KabAIClub</Link>
          </li>
          <li>
            <Link to="/events" onClick={() => setIsOpen(false)}>Events</Link>
          </li>
          <li>
            <Link to="/news" onClick={() => setIsOpen(false)}>News</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default IndabaxNavbar;