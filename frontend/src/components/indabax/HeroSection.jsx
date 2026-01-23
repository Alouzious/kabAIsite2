import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './HeroSection.css';

const HeroSection = () => {
  const [heroSlides, setHeroSlides] = useState([]);
  const [settings, setSettings] = useState(null);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const [loading, setLoading] = useState(true);
  const intervalRef = useRef(null);

  // Fetch hero slides and settings from API
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch hero slides
        const heroRes = await axios.get('/api/indabax/hero/');
        const heroData = heroRes.data.results || heroRes.data || [];
        setHeroSlides(heroData.filter(h => h.is_active || true));

        // Fetch settings for logo
        const settingsRes = await axios.get('/api/indabax/settings/current/');
        setSettings(settingsRes.data);
      } catch (err) {
        console.error('Error loading data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

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
    if (!isAnimating && heroSlides.length > 0) {
      setIsAnimating(true);
      setCurrentSlide(index);
      setTimeout(() => setIsAnimating(false), 800);
    }
  };

  if (loading) {
    return (
      <div className="hero-loading">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (!heroSlides || heroSlides.length === 0) {
    return (
      <div className="hero-no-data">
        <p>No hero slides available</p>
      </div>
    );
  }

  return (
    <section className="indabax-hero-section">
      {/* Logo in top right corner */}
      <div className="hero-logo-container">
        <div className="hero-logo-circle">
          {settings?.logo_url ? (
            <img
              src={settings.logo_url}
              alt={settings?.site_name || "IndabaX Kabale"}
              className="hero-logo-img"
            />
          ) : (
            <>
              <span className="hero-logo-text">IndabaX</span>
              <span className="hero-logo-subtext">Kabale</span>
            </>
          )}
        </div>
      </div>

      <div className="hero-carousel">
        {/* Indicators */}
        {heroSlides.length > 1 && (
          <div className="hero-indicators">
            {heroSlides.map((_, index) => (
              <button
                key={index}
                onClick={() => goToSlide(index)}
                className={`hero-indicator ${currentSlide === index ? 'active' : ''}`}
                aria-label={`Slide ${index + 1}`}
              />
            ))}
          </div>
        )}

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
                  backgroundImage: `url('${slide.image_url || 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1920'}')`,
                }}
              >
                <div className="hero-overlay"></div>
                <div className="hero-container">
                  <div className="hero-content">
                    <h1 className="hero-title">{slide.title}</h1>
                    {slide.description && (
                      <h3 className="hero-subtitle">{slide.description}</h3>
                    )}
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
              className="hero-control hero-control-prev"
              onClick={prevSlide}
              aria-label="Previous slide"
            >
              <svg width="20" height="20" viewBox="0 0 16 16" fill="#fff">
                <path d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/>
              </svg>
            </button>
            <button
              className="hero-control hero-control-next"
              onClick={nextSlide}
              aria-label="Next slide"
            >
              <svg width="20" height="20" viewBox="0 0 16 16" fill="#fff">
                <path d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
              </svg>
            </button>
          </>
        )}
      </div>
    </section>
  );
};

export default HeroSection;