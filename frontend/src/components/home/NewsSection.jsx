import React, { useState, useEffect, useRef } from 'react';
import './NewsSection.css';
import config from "../../api/config";

const NewsSection = ({ initialNews = [] }) => {
  const [news, setNews] = useState(initialNews);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const autoPlayInterval = useRef(null);
  const sectionRef = useRef(null);

  const totalSlides = news.length;

  // Fetch news from API
  useEffect(() => {
    if (initialNews.length === 0) {
      fetchNews();
    }
  }, []);

  const fetchNews = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/news/articles/`);
      const data = await response.json();
      setNews(data.results || []);
    } catch (error) {
      console.error('Error fetching news:', error);
    }
  };

  useEffect(() => {
    startAutoPlay();
    return () => pauseAutoPlay();
  }, [currentSlide]);

  useEffect(() => {
    const hash = window.location.hash;
    if (hash) {
      const target = document.querySelector(hash);
      if (target) {
        setTimeout(() => {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
      }
    }
  }, []);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowLeft') prevSlide();
      if (e.key === 'ArrowRight') nextSlide();
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [currentSlide, isTransitioning]);

  useEffect(() => {
    let startX = 0;
    let endX = 0;

    const handleTouchStart = (e) => {
      startX = e.touches[0].clientX;
    };

    const handleTouchEnd = (e) => {
      endX = e.changedTouches[0].clientX;
      handleSwipe(startX, endX);
    };

    const section = sectionRef.current;
    if (section) {
      section.addEventListener('touchstart', handleTouchStart);
      section.addEventListener('touchend', handleTouchEnd);

      return () => {
        section.removeEventListener('touchstart', handleTouchStart);
        section.removeEventListener('touchend', handleTouchEnd);
      };
    }
  }, [currentSlide, isTransitioning]);

  const handleSwipe = (startX, endX) => {
    const threshold = 50;
    const diff = startX - endX;

    if (Math.abs(diff) > threshold) {
      if (diff > 0) {
        nextSlide();
      } else {
        prevSlide();
      }
    }
  };

  const nextSlide = () => {
    if (isTransitioning || totalSlides === 0) return;
    setIsTransitioning(true);
    setCurrentSlide((prev) => (prev + 1) % totalSlides);
    setTimeout(() => setIsTransitioning(false), 800);
  };

  const prevSlide = () => {
    if (isTransitioning || totalSlides === 0) return;
    setIsTransitioning(true);
    setCurrentSlide((prev) => (prev - 1 + totalSlides) % totalSlides);
    setTimeout(() => setIsTransitioning(false), 800);
  };

  const goToSlide = (index) => {
    if (isTransitioning || index === currentSlide || totalSlides === 0) return;
    setIsTransitioning(true);
    setCurrentSlide(index);
    setTimeout(() => setIsTransitioning(false), 800);
  };

  const startAutoPlay = () => {
    pauseAutoPlay();
    if (totalSlides > 1) {
      autoPlayInterval.current = setInterval(() => {
        nextSlide();
      }, 5000);
    }
  };

  const pauseAutoPlay = () => {
    if (autoPlayInterval.current) {
      clearInterval(autoPlayInterval.current);
      autoPlayInterval.current = null;
    }
  };

  const getCardClass = (index) => {
    if (index === currentSlide) return 'news-card active';
    if (index === (currentSlide - 1 + totalSlides) % totalSlides) return 'news-card prev';
    if (index === (currentSlide + 1) % totalSlides) return 'news-card next';
    return 'news-card';
  };

  // Show date as "Month day, Year" if possible, else raw string
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return isNaN(date)
      ? dateString
      : date.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        });
  };

  const truncateText = (text, maxLength) => {
    if (!text) return '';
    return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;
  };

  if (news.length === 0) {
    return (
      <section id="news-section" className="news-slider-section">
        <div className="news-content-overlay">
          <div className="news-no-data">
            <p>No news available at the moment.</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section
      id="news-section"
      className="news-slider-section"
      ref={sectionRef}
      onMouseEnter={pauseAutoPlay}
      onMouseLeave={startAutoPlay}
    >
      {/* Background Slider */}
      <div className="news-background-slider">
        {news.map((item, index) => (
          <div
            key={`bg-${item.id}`}
            className={`news-background-slide ${index === currentSlide ? 'active' : ''}`}
            style={{ backgroundImage: `url(${item.image_thumbnail_url})` }}
          />
        ))}
      </div>

      {/* Content Overlay */}
      <div className="news-content-overlay">
        <div className="news-heading">
          <h2>Latest News & Updates</h2>
          <p>Stay updated with the most recent announcements and highlights</p>
        </div>

        <div className="news-slider-container">
          {news.map((item, index) => (
            <div
              key={item.id}
              id={`news-section-${item.slug}`}
              className="news-card-wrapper"
            >
              <div className={getCardClass(index)}>
                {item.image_thumbnail_url && (
                  <img 
                    src={item.image_thumbnail_url}
                    alt={item.title} 
                    loading="lazy"
                  />
                )}
                <div className="news-text">
                  <h3>{item.title}</h3>
                  <p>{truncateText(item.excerpt, 150)}</p>
                  <div className="news-meta">
                    <span className="news-date">
                      {formatDate(item.date)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Slider Indicators */}
        <div className="news-slider-indicators">
          {news.map((_, index) => (
            <div
              key={`indicator-${index}`}
              className={`news-indicator ${index === currentSlide ? 'active' : ''}`}
              onClick={() => goToSlide(index)}
            />
          ))}
        </div>

        {/* Slider Controls */}
        <div className="news-slider-controls">
          <button 
            className="news-slider-btn" 
            id="prevBtn" 
            onClick={prevSlide}
            disabled={isTransitioning}
          >
            ‹
          </button>
          <button 
            className="news-slider-btn" 
            id="nextBtn" 
            onClick={nextSlide}
            disabled={isTransitioning}
          >
            ›
          </button>
        </div>
      </div>
    </section>
  );
};

export default NewsSection;