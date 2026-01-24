import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Linkedin, Twitter, Github, Mail, ChevronDown, ChevronUp } from 'lucide-react';

const LeadersSection = () => {
  const [leaders, setLeaders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showArchived, setShowArchived] = useState(false);

  useEffect(() => {
    axios.get('/api/indabax/leaders/')
      .then(res => {
        // DRF may paginate, so check: .results or flat
        const data = res.data.results || res.data || [];
        setLeaders(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading leaders:', err);
        setError('Failed to load leaders.');
        setLoading(false);
      });
  }, []);

  // Now using start_year/end_year, is_current + is_archived properties
  const currentLeaders = leaders.filter(l => l.is_current);
  const archivedLeaders = leaders.filter(l => l.is_archived);

  // Group archived by (end_year, then start_year, fallback to label)
  const archivedByEndYear = {};
  archivedLeaders.forEach(l => {
    const year = l.end_year || 'Unknown Year';
    if (!archivedByEndYear[year]) archivedByEndYear[year] = [];
    archivedByEndYear[year].push(l);
  });

  if (loading) return <div className="text-center p-4">Loading leaders...</div>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <section className="indabax-leaders py-5">
      <div className="container">
        <h2 className="mb-4">Current Leaders</h2>
        <div className="row leaders-list">
          {currentLeaders.length === 0 ? (
            <div className="col-12"><p>No current leaders found.</p></div>
          ) : (
            currentLeaders.map(leader => (
              <div key={leader.id} className="col-md-6 col-lg-4 mb-4">
                <div className="leader-card card h-100">
                  {leader.profile_image_url && (
                    <img 
                      src={leader.profile_image_url} 
                      alt={leader.name} 
                      className="leader-img card-img-top"
                      onError={(e) => {
                        e.target.style.display = 'none';
                      }}
                    />
                  )}
                  <div className="card-body">
                    <h3 className="card-title">{leader.name}</h3>
                    <p className="card-subtitle mb-2 text-muted">{leader.role}</p>
                    <p className="text-muted">
                      {leader.course}
                      {leader.start_year && (
                        <> ({leader.start_year}{leader.end_year ? ` - ${leader.end_year}` : ' - present'})</>
                      )}
                    </p>
                    <p className="card-text">{leader.bio}</p>
                    <div className="leader-socials d-flex gap-2 flex-wrap">
                      {leader.linkedin && (
                        <a href={leader.linkedin} target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-outline-primary" title="LinkedIn">
                          <Linkedin size={18} />
                        </a>
                      )}
                      {leader.twitter && (
                        <a href={leader.twitter} target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-outline-info" title="Twitter/X">
                          <Twitter size={18} />
                        </a>
                      )}
                      {leader.github && (
                        <a href={leader.github} target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-outline-dark" title="GitHub">
                          <Github size={18} />
                        </a>
                      )}
                      {leader.email && (
                        <a href={`mailto:${leader.email}`} className="btn btn-sm btn-outline-secondary" title="Email">
                          <Mail size={18} />
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Toggle Button for Archived Leaders */}
        {Object.keys(archivedByEndYear).length > 0 && (
          <div className="text-center my-4">
            <button 
              onClick={() => setShowArchived(!showArchived)}
              className="btn btn-lg btn-primary"
              style={{
                background: 'linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%)',
                border: 'none',
                borderRadius: '50px',
                padding: '12px 32px',
                fontSize: '1.1rem',
                fontWeight: '600',
                boxShadow: '0 4px 15px rgba(30, 58, 138, 0.3)',
                transition: 'all 0.3s ease',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '8px'
              }}
              onMouseEnter={(e) => {
                e.target.style.transform = 'translateY(-2px)';
                e.target.style.boxShadow = '0 6px 20px rgba(30, 58, 138, 0.4)';
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = '0 4px 15px rgba(30, 58, 138, 0.3)';
              }}
            >
              {showArchived ? (
                <>
                  Hide Previous Leaders
                  <ChevronUp size={20} />
                </>
              ) : (
                <>
                  Show Previous Leaders
                  <ChevronDown size={20} />
                </>
              )}
            </button>
          </div>
        )}

        {/* Archived Leaders by End Year */}
        {showArchived && Object.keys(archivedByEndYear).length > 0 && (
          <>
            <h2 className="mt-5 mb-4">Previous Leaders</h2>
            {Object.keys(archivedByEndYear).sort((a, b) => b - a).map(year => (
              <div key={year} className="archived-year mb-4">
                <h3 className="mb-3">{year}</h3>
                <div className="row leaders-list">
                  {archivedByEndYear[year].map(leader => (
                    <div key={leader.id} className="col-md-6 col-lg-4 mb-4">
                      <div className="leader-card card h-100">
                        {leader.profile_image_url && (
                          <img 
                            src={leader.profile_image_url} 
                            alt={leader.name} 
                            className="leader-img card-img-top"
                            onError={(e) => {
                              e.target.style.display = 'none';
                            }}
                          />
                        )}
                        <div className="card-body">
                          <h3 className="card-title">{leader.name}</h3>
                          <p className="card-subtitle mb-2 text-muted">{leader.role}</p>
                          <p className="text-muted">
                            {leader.course}
                            {leader.start_year && (
                              <> ({leader.start_year}{leader.end_year ? ` - ${leader.end_year}` : ''})</>
                            )}
                          </p>
                          <p className="card-text">{leader.bio}</p>
                          <div className="leader-socials d-flex gap-2 flex-wrap">
                            {leader.linkedin && (
                              <a href={leader.linkedin} target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-outline-primary" title="LinkedIn">
                                <Linkedin size={18} />
                              </a>
                            )}
                            {leader.twitter && (
                              <a href={leader.twitter} target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-outline-info" title="Twitter/X">
                                <Twitter size={18} />
                              </a>
                            )}
                            {leader.github && (
                              <a href={leader.github} target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-outline-dark" title="GitHub">
                                <Github size={18} />
                              </a>
                            )}
                            {leader.email && (
                              <a href={`mailto:${leader.email}`} className="btn btn-sm btn-outline-secondary" title="Email">
                                <Mail size={18} />
                              </a>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </>
        )}
      </div>
    </section>
  );
};

export default LeadersSection;