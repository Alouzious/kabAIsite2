import React, { useState, useEffect } from 'react';
import './TeamSection.css';

const TeamSection = () => {
  const [currentLeaders, setCurrentLeaders] = useState([]);
  const [archivedLeaders, setArchivedLeaders] = useState([]);
  const [showArchived, setShowArchived] = useState(false);
  const [loading, setLoading] = useState(false);
  const [hoveredCard, setHoveredCard] = useState(null);

  // Fetch leaders from API
  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetch('/api/team/members/current/').then(res => res.json()),
      fetch('/api/team/members/archived/').then(res => res.json())
    ])
      .then(([current, archived]) => {
        setCurrentLeaders(current || []);
        setArchivedLeaders(archived || []);
      })
      .catch((error) => {
        console.error("Error fetching team members", error);
      })
      .finally(() => setLoading(false));
  }, []);

  // Leader Card component
  const LeaderCard = ({ leader }) => (
    <div 
      className="leader-card"
      onMouseEnter={() => setHoveredCard(leader.id)}
      onMouseLeave={() => setHoveredCard(null)}
    >
      {/* Profile Image */}
      <div className="leader-photo-wrapper">
        <div className="leader-photo">
          {leader.photo_thumbnail_url ? (
            <img src={leader.photo_thumbnail_url} alt={leader.name} loading="lazy" />
          ) : (
            <div className="leader-placeholder-photo">
              {leader.name.charAt(0).toUpperCase()}
            </div>
          )}
        </div>
        
        {/* Social Media Icons - Show on Hover */}
        <div className={`leader-social-overlay ${hoveredCard === leader.id ? 'show' : ''}`}>
          <div className="social-icons-grid">
            {leader.email && (
              <a href={`mailto:${leader.email}`} className="social-icon email" title="Email">
                <i className="fas fa-envelope"></i>
              </a>
            )}
            {leader.linkedin_url && (
              <a href={leader.linkedin_url} className="social-icon linkedin" target="_blank" rel="noopener noreferrer" title="LinkedIn">
                <i className="fab fa-linkedin-in"></i>
              </a>
            )}
            {leader.twitter_url && (
              <a href={leader.twitter_url} className="social-icon twitter" target="_blank" rel="noopener noreferrer" title="X (Twitter)">
                <i className="fab fa-x-twitter"></i>
              </a>
            )}
            {leader.github_url && (
              <a href={leader.github_url} className="social-icon github" target="_blank" rel="noopener noreferrer" title="GitHub">
                <i className="fab fa-github"></i>
              </a>
            )}
            {leader.website_url && (
              <a href={leader.website_url} className="social-icon website" target="_blank" rel="noopener noreferrer" title="Website">
                <i className="fas fa-globe"></i>
              </a>
            )}
            {leader.phone && (
              <a href={`tel:${leader.phone}`} className="social-icon phone" title="Phone">
                <i className="fas fa-phone-alt"></i>
              </a>
            )}
          </div>
        </div>
      </div>
      
      {/* Leader Information */}
      <div className="leader-info">
        <h4 className="leader-name">{leader.name}</h4>
        <p className="leader-position">{leader.display_title}</p>
        
        {leader.start_year && (
          <div className="leader-tenure">
            <i className="fas fa-calendar-alt"></i>
            <span>
              {leader.is_current
                ? `${leader.start_year} - Present`
                : `${leader.start_year} - ${leader.end_year}`}
            </span>
          </div>
        )}
        
        {leader.bio && (
          <p className="leader-bio">
            {leader.bio.length > 120 ? `${leader.bio.substring(0, 120)}...` : leader.bio}
          </p>
        )}
      </div>
    </div>
  );

  if (loading) {
    return (
      <section className="leaders-section">
        <div className="leaders-loading">
          <div className="spinner"></div>
          <p>Loading team members...</p>
        </div>
      </section>
    );
  }

  return (
    <section id="leaders-section" className="leaders-section">
      {/* Section Header */}
      <div className="leaders-section-header">
        {/* <div className="leaders-section-subtitle">TEAM MEMBERS</div> */}
        <h2 className="leaders-section-title">
          Meet our<br />
          Professional team of<br />
          experts
        </h2>
        {/* <p className="leaders-section-description">
          Our dedicated team of leaders and experts are committed to driving innovation and excellence in everything we do.
        </p> */}
      </div>

      {/* Current Team */}
      <div className="leaders-category-section">
        <h3 className="leaders-category-title">Current Team</h3>
        {currentLeaders.length > 0 ? (
          <div className="leaders-grid">
            {currentLeaders.map((leader) => (
              <LeaderCard key={leader.id} leader={leader} />
            ))}
          </div>
        ) : (
          <div className="leaders-no-data">
            <p>No current team members to display.</p>
          </div>
        )}
      </div>

      {/* Show/hide archived team button */}
      {archivedLeaders.length > 0 && (
        <div className="leaders-view-previous">
          <button
            className="leaders-view-previous-btn"
            onClick={() => setShowArchived(!showArchived)}
          >
            <i className={`fas fa-${showArchived ? 'chevron-up' : 'chevron-down'}`}></i>
            {showArchived ? 'Hide Previous Leaders' : 'Show Previous Leaders'}
          </button>
        </div>
      )}

      {/* Archived Team */}
      {showArchived && (
        <div className="leaders-category-section archived-section">
          <h3 className="leaders-category-title">Previous Leaders</h3>
          <div className="leaders-grid">
            {archivedLeaders.map((leader) => (
              <LeaderCard key={leader.id} leader={leader} />
            ))}
          </div>
        </div>
      )}
    </section>
  );
};

export default TeamSection;