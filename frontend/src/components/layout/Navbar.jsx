import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';
import config from "../../api/config";

const Navbar = () => {
  const location = useLocation();

  // States for fetched site data
  const [siteSettings, setSiteSettings] = useState({});
  const [aboutPages, setAboutPages] = useState([]);
  const [news, setNews] = useState([]);
  const [events, setEvents] = useState([]);
  const [research, setResearch] = useState([]);
  const [resources, setResources] = useState([]);
  const [community, setCommunity] = useState([]);
  const [projects, setProjects] = useState([]);
  
  const [scrolled, setScrolled] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState(null);
  const [searchModalOpen, setSearchModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Fetch all data on mount (like other sections)
  useEffect(() => {
    fetch(`${config.API_BASE_URL}/core/site-settings/`)
      .then(res => res.json())
      .then(data => {
        console.log('Site settings response:', data); // Debug log
        
        // Handle paginated response with results array
        if (data.results && Array.isArray(data.results) && data.results.length > 0) {
          setSiteSettings(data.results[0]);
        } 
        // Handle direct array response
        else if (Array.isArray(data) && data.length > 0) {
          setSiteSettings(data[0]);
        } 
        // Handle single object response
        else if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
          setSiteSettings(data);
        } 
        // Fallback to empty object
        else {
          setSiteSettings({});
        }
      })
      .catch(error => {
        console.error('Error fetching site settings:', error);
        setSiteSettings({});
      });

    fetch(`${config.API_BASE_URL}/about/`)
      .then(res => res.json())
      .then(data => setAboutPages(data.results || data || []));
    fetch(`${config.API_BASE_URL}/news/articles/`)
      .then(res => res.json())
      .then(data => setNews(data.results || data || []));
    fetch(`${config.API_BASE_URL}/events/`)
      .then(res => res.json())
      .then(data => setEvents(data.results || data || []));
    fetch(`${config.API_BASE_URL}/research/`)
      .then(res => res.json())
      .then(data => setResearch(data.results || data || []));
    fetch(`${config.API_BASE_URL}/resources/`)
      .then(res => res.json())
      .then(data => setResources(data.results || data || []));
    fetch(`${config.API_BASE_URL}/community/`)
      .then(res => res.json())
      .then(data => setCommunity(data.results || data || []));
    fetch(`${config.API_BASE_URL}/projects/`)
      .then(res => res.json())
      .then(data => setProjects(data.results || data || []));
  }, []);

  // Scroll effect
  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleMouseEnter = (dropdownId) => { setActiveDropdown(dropdownId); };
  const handleMouseLeave = () => { setTimeout(() => setActiveDropdown(null), 200); };
  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      // Implement search logic...
      setSearchModalOpen(false);
      setSearchQuery('');
    }
  };
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) element.scrollIntoView({ behavior: 'smooth' });
  };
  const isActive = (path) => location.pathname === path;
  const newsSummary = (item) => item.excerpt ? item.excerpt.substring(0, 60) : '';
  const newsImage = (item) => item.image_thumbnail_url || item.image || '';

  // Safe filter for aboutPages - ensure it's an array
  const leftAboutPages = Array.isArray(aboutPages) ? aboutPages.filter(page => page.column_position === 'left') : [];
  const rightAboutPages = Array.isArray(aboutPages) ? aboutPages.filter(page => page.column_position === 'right') : [];
  
  // Safe filter for resources - ensure it's an array
  const learningResources = Array.isArray(resources) ? resources.filter(r => r.resource_type === 'learning') : [];
  const toolResources = Array.isArray(resources) ? resources.filter(r => r.resource_type === 'tool') : [];

  return (
    <>
      {/* Top Site Content */}
      <div className="top_site_content py-2">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-md-6 text-start">
              {siteSettings.contact_email && (
                <span>
                  <i className="fa-solid fa-envelope me-1 text-primary"></i>
                  <a href={`mailto:${siteSettings.contact_email}`} className="contact-link text-primary">
                    {siteSettings.contact_email}
                  </a>
                </span>
              )}
              {siteSettings.contact_phone && (
                <span className="ms-3">
                  <i className="fa-solid fa-phone me-1 text-primary"></i>
                  <a href={`tel:${siteSettings.contact_phone}`} className="contact-link text-primary">
                    {siteSettings.contact_phone}
                  </a>
                </span>
              )}
            </div>
            <div className="col-md-6 d-flex justify-content-end align-items-center gap-3">
              <div className="social-media-links d-flex align-items-center gap-2">
                {siteSettings.facebook_url && (
                  <a href={siteSettings.facebook_url} target="_blank" rel="noopener noreferrer" className="text-black social-link">
                    <i className="fab fa-facebook-f"></i>
                  </a>
                )}
                {siteSettings.twitter_url && (
                  <a href={siteSettings.twitter_url} target="_blank" rel="noopener noreferrer" className="text-black social-link">
                    <i className="fab fa-twitter"></i>
                  </a>
                )}
                {siteSettings.instagram_url && (
                  <a href={siteSettings.instagram_url} target="_blank" rel="noopener noreferrer" className="text-black social-link">
                    <i className="fab fa-instagram"></i>
                  </a>
                )}
                {siteSettings.linkedin_url && (
                  <a href={siteSettings.linkedin_url} target="_blank" rel="noopener noreferrer" className="text-black social-link">
                    <i className="fab fa-linkedin-in"></i>
                  </a>
                )}
                {siteSettings.youtube_url && (
                  <a href={siteSettings.youtube_url} target="_blank" rel="noopener noreferrer" className="text-black social-link">
                    <i className="fab fa-youtube"></i>
                  </a>
                )}
                {siteSettings.whatsapp_url && (
                  <a href={siteSettings.whatsapp_url} target="_blank" rel="noopener noreferrer" className="text-black social-link">
                    <i className="fab fa-whatsapp"></i>
                  </a>
                )}
              </div>
              {siteSettings.quick_links && siteSettings.quick_links.length > 0 && (
                <div className="dropdown">
                  <button className="btn btn-sm btn-outline-dark dropdown-toggle" data-bs-toggle="dropdown">
                    Quick Links
                  </button>
                  <ul className="dropdown-menu dropdown-menu-end quick-links-dropdown">
                    {siteSettings.quick_links.map((link, index) => (
                      <li key={index}>
                        <a className="dropdown-item" href={link.url} target="_blank" rel="noopener noreferrer">
                          {link.name}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Main Navbar */}
      <nav className={`navbar navbar-expand-lg navbar-dark bg-primary sticky-top ${scrolled ? 'scrolled' : ''}`}>
        <div className="container-fluid">
          <button 
            className="navbar-toggler" 
            type="button" 
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className={`collapse navbar-collapse justify-content-center ${isMobileMenuOpen ? 'show' : ''}`}>
            <ul className="navbar-nav d-flex flex-row">

              {/* Home */}
              <li className="nav-item">
                <Link className={`nav-link ${isActive('/') ? 'active' : ''}`} to="/">
                  Home
                </Link>
              </li>

              {/* About Us */}
              <li 
                className="nav-item nav-hover-content"
                onMouseEnter={() => handleMouseEnter('about')}
                onMouseLeave={handleMouseLeave}
              >
                <Link to="/about" className="nav-link">About Us</Link>
                {activeDropdown === 'about' && aboutPages.length > 0 && (
                  <div className="hover-content-panel show"
                    onMouseEnter={() => setActiveDropdown('about')}
                    onMouseLeave={handleMouseLeave}
                  >
                    <div className="container">
                      <div className="row">
                        <div className="col-md-6">
                          <h6 className="dropdown-header">WHO WE ARE</h6>
                          <ul className="list-unstyled">
                            {leftAboutPages.map(page => (
                              <li key={page.id}>
                                <Link to={`/about#${page.title.toLowerCase().replace(/\s+/g, '-')}`}>
                                  {page.title}
                                </Link>
                              </li>
                            ))}
                          </ul>
                        </div>
                        <div className="col-md-6">
                          <h6 className="dropdown-header">WHY WE EXIST</h6>
                          <ul className="list-unstyled">
                            {rightAboutPages.map(page => (
                              <li key={page.id}>
                                <Link to={`/about#${page.title.toLowerCase().replace(/\s+/g, '-')}`}>
                                  {page.title}
                                </Link>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </li>

              {/* Leaders */}
              <li 
                className="nav-item nav-hover-content"
                onMouseEnter={() => handleMouseEnter('leaders')}
                onMouseLeave={handleMouseLeave}
              >
                <a 
                  href="#team-section" 
                  className="nav-link"
                  onClick={(e) => {
                    e.preventDefault();
                    scrollToSection('team-section');
                  }}
                >
                  Leaders
                </a>
                {activeDropdown === 'leaders' && (
                  <div
                    className="hover-content-panel show"
                    onMouseEnter={() => setActiveDropdown('leaders')}
                    onMouseLeave={handleMouseLeave}
                  >
                    <ul className="list-unstyled mb-0">
                      <li><a href="#category-student">Student Leaders</a></li>
                      <li><a href="#category-faculty">Faculty Mentors</a></li>
                    </ul>
                  </div>
                )}
              </li>

              {/* News */}
              <li 
                className="nav-item nav-hover-content"
                onMouseEnter={() => handleMouseEnter('news')}
                onMouseLeave={handleMouseLeave}
              >
                <a 
                  href="#news-section" 
                  className="nav-link"
                  onClick={(e) => {
                    e.preventDefault();
                    scrollToSection('news-section');
                  }}
                >
                  News
                </a>
                {activeDropdown === 'news' && (
                  <div 
                    className="hover-content-panel show"
                    onMouseEnter={() => setActiveDropdown('news')}
                    onMouseLeave={handleMouseLeave}
                  >
                    {news && news.length > 0 ? (
                      <ul className="list-unstyled mb-0">
                        {news.map(item => (
                          <li key={item.id} className="d-flex align-items-start mb-3">
                            {newsImage(item) && (
                              <img 
                                src={newsImage(item)} 
                                alt={item.title} 
                                style={{width:'50px', height:'50px', objectFit:'cover', borderRadius:'4px', marginRight:'10px'}}
                              />
                            )}
                            <div>
                              <a href={`#news-section-${item.slug}`} className="fw-bold text-dark text-decoration-none">
                                {item.title}
                              </a>
                              <p className="mb-0 text-muted" style={{fontSize: '0.85rem'}}>
                                {newsSummary(item)}...
                              </p>
                            </div>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <div className="text-muted text-center py-3">
                        <i className="bi bi-info-circle" style={{fontSize: '1.2rem'}}></i><br />
                        No news updates available at the moment.
                      </div>
                    )}
                  </div>
                )}
              </li>

              {/* Events */}
              <li 
                className="nav-item nav-hover-content"
                onMouseEnter={() => handleMouseEnter('events')}
                onMouseLeave={handleMouseLeave}
              >
                <a 
                  href="#event-section" 
                  className="nav-link"
                  onClick={(e) => {
                    e.preventDefault();
                    scrollToSection('event-section');
                  }}
                >
                  Events
                </a>
                {activeDropdown === 'events' && (
                  <div 
                    className="hover-content-panel show"
                    onMouseEnter={() => setActiveDropdown('events')}
                    onMouseLeave={handleMouseLeave}
                  >
                    <ul className="list-unstyled">
                      {events && events.length > 0 ? (
                        events.map(event => (
                          <li key={event.id}>
                            <a href={`#event-section-${event.slug}`}>{event.title}</a>
                          </li>
                        ))
                      ) : (
                        <li><em>No upcoming events available</em></li>
                      )}
                    </ul>
                  </div>
                )}
              </li>

              {/* Research */}
              <li 
                className="nav-item nav-hover-content"
                onMouseEnter={() => handleMouseEnter('research')}
                onMouseLeave={handleMouseLeave}
              >
                {research && research.length > 0 ? (
                  <Link to={`/research/${research[0].id}`} className="nav-link">Research</Link>
                ) : (
                  <a href="#" className="nav-link">Research</a>
                )}
                {activeDropdown === 'research' && research && research.length > 0 && (
                  <div 
                    className="hover-content-panel show"
                    onMouseEnter={() => setActiveDropdown('research')}
                    onMouseLeave={handleMouseLeave}
                  >
                    <ul className="list-unstyled">
                      {research.map(item => (
                        <li key={item.id}>
                          <Link to={`/research/${item.id}`}>{item.title}</Link>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </li>

              {/* Resources */}
              <li 
                className="nav-item nav-hover-content"
                onMouseEnter={() => handleMouseEnter('resources')}
                onMouseLeave={handleMouseLeave}
              >
                <a href="#" className="nav-link">Resources</a>
                {activeDropdown === 'resources' && resources && resources.length > 0 && (
                  <div 
                    className="hover-content-panel show"
                    onMouseEnter={() => setActiveDropdown('resources')}
                    onMouseLeave={handleMouseLeave}
                  >
                    <div className="row">
                      <div className="col-md-6">
                        <h6 className="dropdown-header">LEARNING RESOURCES</h6>
                        <ul className="list-unstyled">
                          {learningResources.map(resource => (
                            <li key={resource.id}>
                              <Link to={`/resource/${resource.id}`}>{resource.title}</Link>
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div className="col-md-6">
                        <h6 className="dropdown-header">TOOLS & DOWNLOADS</h6>
                        <ul className="list-unstyled">
                          {toolResources.map(resource => (
                            <li key={resource.id}>
                              <Link to={`/resource/${resource.id}`}>{resource.title}</Link>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                )}
              </li>

              {/* Communities */}
              <li 
                className="nav-item nav-hover-content"
                onMouseEnter={() => handleMouseEnter('community')}
                onMouseLeave={handleMouseLeave}
              >
                <a href="#" className="nav-link">Communities</a>
                {activeDropdown === 'community' && (
                  <div 
                    className="hover-content-panel show"
                    onMouseEnter={() => setActiveDropdown('community')}
                    onMouseLeave={handleMouseLeave}
                  >
                    <ul className="list-unstyled">
                      {community && community.length > 0 ? (
                        community.map(item => (
                          <li key={item.id}>
                            <Link to={`/community/${item.id}`}>{item.name || item.title}</Link>
                          </li>
                        ))
                      ) : (
                        <li>
                          <Link to="/communities/indabax">IndabaX</Link>
                        </li>
                      )}
                    </ul>
                  </div>
                )}
              </li>

              {/* Projects */}
              <li 
                className="nav-item nav-hover-content"
                onMouseEnter={() => handleMouseEnter('projects')}
                onMouseLeave={handleMouseLeave}
              >
                <a 
                  href="#projects-section" 
                  className="nav-link"
                  onClick={(e) => {
                    e.preventDefault();
                    scrollToSection('projects-section');
                  }}
                >
                  Projects
                </a>
                {activeDropdown === 'projects' && projects && projects.length > 0 && (
                  <div 
                    className="hover-content-panel show"
                    onMouseEnter={() => setActiveDropdown('projects')}
                    onMouseLeave={handleMouseLeave}
                  >
                    <ul className="list-unstyled">
                      {projects.map(project => (
                        <li key={project.id}>
                          <Link to={`/project/${project.id}`}>{project.title}</Link>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </li>

              {/* Search Button */}
              <li className="nav-item">
                <button 
                  className="btn btn-outline-light ms-3" 
                  type="button" 
                  onClick={() => setSearchModalOpen(true)}
                >
                  <i className="fas fa-search"></i>
                </button>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      {/* Search Modal */}
      {searchModalOpen && (
        <div className="modal fade show" style={{display: 'block'}} onClick={() => setSearchModalOpen(false)}>
          <div className="modal-dialog" onClick={e => e.stopPropagation()}>
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Search</h5>
                <button type="button" className="btn-close" onClick={() => setSearchModalOpen(false)}></button>
              </div>
              <div className="modal-body">
                <form onSubmit={handleSearch}>
                  <div className="input-group">
                    <input 
                      type="text" 
                      className="form-control" 
                      placeholder="Search..." 
                      value={searchQuery}
                      onChange={e => setSearchQuery(e.target.value)}
                      autoFocus
                    />
                    <button className="btn btn-primary" type="submit">
                      <i className="fas fa-search"></i>
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      )}
      {searchModalOpen && <div className="modal-backdrop fade show"></div>}
    </>
  );
};

export default Navbar;