import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './HeroSlider.css';
import config from "../../api/config";

const HeroSlider = () => {
  const [heroSlides, setHeroSlides] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const intervalRef = useRef(null);

  // Fetch hero slides from API
  useEffect(() => {
    axios.get(`${config.API_BASE_URL}/core/hero-slides/`)
      .then(res => {
        // Handle paginated response
        const data = res.data.results || res.data || [];
        console.log(' Fetched hero slides:', data);
        setHeroSlides(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(err => {
        console.error(' Error loading hero slides:', err);
        setError('Failed to load hero slides.');
        setLoading(false);
      });
  }, []);

  // Get responsive background image
  const getResponsiveImage = (slide) => {
    const width = window.innerWidth;
    
    if (width <= 768 && slide.image_mobile_url) {
      return slide.image_mobile_url;
    } else if (width <= 1024 && slide.image_tablet_url) {
      return slide.image_tablet_url;
    } else if (slide.image_desktop_url) {
      return slide.image_desktop_url;
    }
    
    return slide.image;
  };

  const nextSlide = () => {
    if (!isAnimating && heroSlides.length > 0) {
      setIsAnimating(true);
      setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
      setTimeout(() => setIsAnimating(false), 800);
    }
  };

  const prevSlide = () => {
    if (!isAnimating && heroSlides.length > 0) {
      setIsAnimating(true);
      setCurrentSlide((prev) => (prev - 1 + heroSlides.length) % heroSlides.length);
      setTimeout(() => setIsAnimating(false), 800);
    }
  };

  const goToSlide = (index) => {
    if (!isAnimating && heroSlides.length > 0 && index !== currentSlide) {
      setIsAnimating(true);
      setCurrentSlide(index);
      setTimeout(() => setIsAnimating(false), 800);
    }
  };

  // Auto-play carousel
  useEffect(() => {
    if (heroSlides.length > 1) {
      intervalRef.current = setInterval(() => {
        nextSlide();
      }, 5000);

      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }
      };
    }
  }, [currentSlide, heroSlides.length]);

  if (loading) {
    return (
      <section className="hero-section">
        <div className="hero-loading">
          <div className="loading-spinner">Loading...</div>
        </div>
      </section>
    );
  }

  if (error) {
    console.error('Hero slider error:', error);
    return null;
  }

  if (!heroSlides || heroSlides.length === 0) {
    console.log('⚠️ No hero slides available');
    return null;
  }

  return (
    <section className="hero-section">
      <div id="heroCarousel" className="hero-carousel slide">
        {/* Indicators */}
        <div className="hero-carousel-indicators">
          {heroSlides.map((_, index) => (
            <button
              key={index}
              type="button"
              onClick={() => goToSlide(index)}
              className={currentSlide === index ? 'active' : ''}
              aria-label={`Slide ${index + 1}`}
            />
          ))}
        </div>

        {/* Slides */}
        <div className="hero-carousel-inner">
          {heroSlides.map((slide, index) => (
            <div
              key={index}
              className={`hero-carousel-item ${currentSlide === index ? 'active' : ''}`}
            >
              <div
                className="hero-slide"
                style={{ 
                  backgroundImage: `url('${getResponsiveImage(slide)}')` 
                }}
              >
                <div className="hero-overlay"></div>
                <div className="container">
                  <div className="row align-items-center min-vh-100">
                    <div className="col-lg-8 mx-auto text-center">
                      <div className="hero-content">
                        <h1 className="hero-title">{slide.title}</h1>
                        {slide.subtitle && (
                          <h3 className="hero-subtitle">{slide.subtitle}</h3>
                        )}
                        <div className="hero-buttons mt-4">
                          {slide.button1_text && (
                            <a
                              href={slide.button1_url || '#'}
                              className={`btn btn-${slide.button1_style || 'primary'} btn-lg me-3`}
                            >
                              {slide.button1_text}
                            </a>
                          )}
                          {slide.button2_text && (
                            <a
                              href={slide.button2_url || '#'}
                              className={`btn btn-${slide.button2_style || 'outline-light'} btn-lg`}
                            >
                              {slide.button2_text}
                            </a>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Navigation Controls */}
        {heroSlides.length > 1 && (
          <>
            <button
              className="hero-carousel-control-prev"
              type="button"
              onClick={prevSlide}
              disabled={isAnimating}
              aria-label="Previous slide"
            >
              <span className="hero-carousel-control-prev-icon" aria-hidden="true"></span>
              <span className="visually-hidden">Previous</span>
            </button>
            <button
              className="hero-carousel-control-next"
              type="button"
              onClick={nextSlide}
              disabled={isAnimating}
              aria-label="Next slide"
            >
              <span className="hero-carousel-control-next-icon" aria-hidden="true"></span>
              <span className="visually-hidden">Next</span>
            </button>
          </>
        )}
      </div>
    </section>
  );
};

export default HeroSlider;