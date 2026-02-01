import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './ProjectsSection.css';
import config from "../../api/config";

const ProjectsSection = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const sliderWrapperRef = useRef(null);
  const sliderRef = useRef(null);
  const scrollTimeoutRef = useRef(null);

  const CONFIG = {
    scrollAmount: 380,
    scrollDebounce: 100,
    animationDelay: 200,
  };

  // Fetch projects from API
  useEffect(() => {
    axios.get(`${config.API_BASE_URL}/projects/`)
      .then(res => {
        const data = res.data.results || res.data || [];
        console.log('Fetched projects:', data);
        
        // If is_published field exists, filter by it; otherwise use all projects
        const publishedProjects = data.filter(project => 
          project.is_published === undefined || project.is_published === true
        );
        setProjects(publishedProjects);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading projects:', err);
        setError('Failed to load projects.');
        setLoading(false);
      });
  }, []);

  // Update mid-card highlight
  const updateMidCardHighlight = () => {
    if (!sliderRef.current || !sliderWrapperRef.current) return;

    const cards = sliderRef.current.querySelectorAll('.project-card');
    cards.forEach(card => card.classList.remove('mid-card'));

    const wrapperRect = sliderWrapperRef.current.getBoundingClientRect();
    const visibleCards = [];

    cards.forEach(card => {
      const rect = card.getBoundingClientRect();
      if (rect.left >= wrapperRect.left && rect.right <= wrapperRect.right) {
        visibleCards.push(card);
      }
    });

    if (visibleCards.length >= 3) {
      visibleCards[1].classList.add('mid-card');
    }
  };

  // Handle scroll events
  const handleScroll = () => {
    if (scrollTimeoutRef.current) return;
    
    scrollTimeoutRef.current = requestAnimationFrame(() => {
      updateMidCardHighlight();
      scrollTimeoutRef.current = null;
    });
  };

  useEffect(() => {
    const wrapper = sliderWrapperRef.current;
    if (!wrapper) return;

    let lastScrollTime = 0;
    const throttledScroll = () => {
      const now = Date.now();
      if (now - lastScrollTime > CONFIG.scrollDebounce) {
        lastScrollTime = now;
        handleScroll();
      }
    };

    wrapper.addEventListener('scroll', throttledScroll, { passive: true });
    
    requestAnimationFrame(() => {
      updateMidCardHighlight();
    });

    return () => {
      wrapper.removeEventListener('scroll', throttledScroll);
      if (scrollTimeoutRef.current) {
        cancelAnimationFrame(scrollTimeoutRef.current);
      }
    };
  }, [projects]);

  // Slide left
  const slideLeft = () => {
    if (!sliderWrapperRef.current) return;

    const currentScroll = sliderWrapperRef.current.scrollLeft;
    const newScroll = Math.max(0, currentScroll - CONFIG.scrollAmount);

    sliderWrapperRef.current.scrollTo({ left: newScroll, behavior: 'smooth' });

    setTimeout(() => {
      requestAnimationFrame(() => {
        updateMidCardHighlight();
      });
    }, CONFIG.animationDelay);
  };

  // Slide right
  const slideRight = () => {
    if (!sliderWrapperRef.current) return;

    const currentScroll = sliderWrapperRef.current.scrollLeft;
    const maxScroll = sliderWrapperRef.current.scrollWidth - sliderWrapperRef.current.clientWidth;
    const newScroll = Math.min(maxScroll, currentScroll + CONFIG.scrollAmount);

    sliderWrapperRef.current.scrollTo({ left: newScroll, behavior: 'smooth' });

    setTimeout(() => {
      requestAnimationFrame(() => {
        updateMidCardHighlight();
      });
    }, CONFIG.animationDelay);
  };

  // Update button states
  const getButtonStates = () => {
    if (!sliderWrapperRef.current) return { leftDisabled: true, rightDisabled: true };

    const scrollLeft = sliderWrapperRef.current.scrollLeft;
    const maxScroll = sliderWrapperRef.current.scrollWidth - sliderWrapperRef.current.clientWidth;

    return {
      leftDisabled: scrollLeft <= 0,
      rightDisabled: scrollLeft >= maxScroll - 10
    };
  };

  // Format date
  const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  // Truncate text
  const truncateText = (text, maxLength = 100) => {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  };

  if (loading) {
    return (
      <section className="projects-slider-section" id="projects-section">
        <div className="container">
          <h2 className="section-title">Our Latest Projects</h2>
          <div className="loading-card">
            <div className="loading-spinner">Loading projects...</div>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="projects-slider-section" id="projects-section">
        <div className="container">
          <h2 className="section-title">Our Latest Projects</h2>
          <div className="alert alert-danger">{error}</div>
        </div>
      </section>
    );
  }

  const buttonStates = getButtonStates();

  return (
    <section className="projects-slider-section" id="projects-section">
      <div className="container">
        <h2 className="section-title">Our Latest Projects</h2>
        
        {projects.length === 0 ? (
          <div className="text-center py-5">
            <p>No projects available at the moment.</p>
          </div>
        ) : (
          <>
            <div className="projects-slider-wrapper" ref={sliderWrapperRef}>
              <div className="projects-slider" ref={sliderRef}>
                {projects.map((project, index) => (
                  <div
                    key={project.id}
                    className={`project-card ${index === 1 ? 'mid-card' : ''}`}
                  >
                    {project.image_thumbnail_url && (
                      <img
                        src={project.image_thumbnail_url}
                        alt={project.title}
                        className="project-image"
                        loading="lazy"
                        onError={(e) => {
                          e.target.style.display = 'none';
                        }}
                      />
                    )}
                    <div className="project-content">
                      <h3 className="project-title">{project.title}</h3>
                      <p className="project-summary">
                        {truncateText(project.short_description, 100)}
                      </p>
                      
                      {project.technologies_list && project.technologies_list.length > 0 && (
                        <div className="project-technologies">
                          {project.technologies_list.slice(0, 3).map((tech, idx) => (
                            <span key={idx} className="tech-badge">{tech}</span>
                          ))}
                          {project.technologies_list.length > 3 && (
                            <span className="tech-badge">+{project.technologies_list.length - 3}</span>
                          )}
                        </div>
                      )}
                      
                      <div className="project-meta">
                        {project.status && (
                          <span className={`project-status status-${project.status}`}>
                            {project.status.replace('_', ' ')}
                          </span>
                        )}
                        {(project.demo_url || project.github_url) && (
                          <a
                            href={project.demo_url || project.github_url}
                            className="project-link"
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {project.demo_url ? 'View Demo' : 'View Code'}
                            <i className="fas fa-arrow-right"></i>
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="slider-nav-container">
              <button
                className="slider-btn"
                type="button"
                onClick={slideLeft}
                disabled={buttonStates.leftDisabled}
              >
                <i className="fas fa-chevron-left"></i>
              </button>
              <button
                className="slider-btn"
                type="button"
                onClick={slideRight}
                disabled={buttonStates.rightDisabled}
              >
                <i className="fas fa-chevron-right"></i>
              </button>
            </div>
          </>
        )}
      </div>
    </section>
  );
};

export default ProjectsSection;