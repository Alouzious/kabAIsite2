import React, { useState, useEffect, useRef } from 'react';
import './GallerySection.css';
import config from "../../api/config";

const GallerySection = () => {
  const [gallery, setGallery] = useState([]);
  const [showExtra, setShowExtra] = useState(false);
  const [loadedImages, setLoadedImages] = useState(new Set());
  const extraGalleryRef = useRef(null);
  const mainGalleryRef = useRef(null);

  // Fetch gallery images from API (images only)
  useEffect(() => {
    const fetchGallery = async () => {
      try {
        // Your correct images endpoint for DRF router is usually /api/gallery/images/
        const response = await fetch(`${config.API_BASE_URL}/gallery/images/`);
        const data = await response.json();
        // support paginated (results) or flat
        setGallery(data.results || data || []);
      } catch (error) {
        console.error('Error fetching gallery:', error);
      }
    };

    fetchGallery();
  }, []);

  // Intersection Observer for fade-in animation
  useEffect(() => {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('gallery-showcase-visible');
        }
      });
    }, observerOptions);

    const items = document.querySelectorAll('.gallery-showcase-item');
    items.forEach(item => observer.observe(item));

    return () => observer.disconnect();
  }, [gallery, showExtra]);

  const handleShowMore = () => {
    setShowExtra(true);
    setTimeout(() => {
      extraGalleryRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  };

  const handleHide = () => {
    mainGalleryRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    setTimeout(() => {
      setShowExtra(false);
    }, 300);
  };

  const handleImageLoad = (imageId) => {
    setLoadedImages(prev => new Set([...prev, imageId]));
  };

  const handleImageClick = (imageUrl) => {
    window.open(imageUrl, '_blank');
  };

  const mainImages = gallery.slice(0, 4);
  const extraImages = gallery.slice(4);
  const hasMore = gallery.length > 4;

  if (gallery.length === 0) {
    return (
      <section className="gallery-showcase-section">
        <h2 className="gallery-showcase-title">Latest Gallery</h2>
        <div className="gallery-showcase-no-data">
          <p>No images available in the gallery yet.</p>
        </div>
      </section>
    );
  }

  return (
    <section id="gallery-showcase-section" className="gallery-showcase-section">
      <h2 className="gallery-showcase-title">Latest Gallery</h2>

      {/* Main Gallery (First 4 images only) */}
      <div id="gallery-showcase-main" className="gallery-showcase-wrapper" ref={mainGalleryRef}>
        {mainImages.map((image) => (
          <div
            key={image.id}
            className={`gallery-showcase-item ${!loadedImages.has(image.id) ? 'gallery-showcase-loading' : ''}`}
            onClick={() => handleImageClick(image.image_url || image.image)}
          >
            <img
              src={image.image_url || image.image}
              alt=""
              loading="lazy"
              onLoad={() => handleImageLoad(image.id)}
              onError={() => handleImageLoad(image.id)}
            />
          </div>
        ))}

        {/* Show More Button */}
        {hasMore && !showExtra && (
          <div className="gallery-showcase-more-btn-container">
            <button
              id="gallery-showcase-show-more-btn"
              className="gallery-showcase-btn gallery-showcase-small-btn"
              onClick={handleShowMore}
              aria-expanded={showExtra}
              aria-controls="gallery-showcase-extra"
            >
              + More
            </button>
          </div>
        )}
      </div>

      {/* Extra Gallery (Rest) */}
      {hasMore && showExtra && (
        <div
          id="gallery-showcase-extra"
          className={`gallery-showcase-wrapper gallery-showcase-extra${showExtra ? ' gallery-showcase-show' : ''}`}
          ref={extraGalleryRef}
          aria-hidden={!showExtra}
        >
          {extraImages.map((image) => (
            <div
              key={image.id}
              className={`gallery-showcase-item ${!loadedImages.has(image.id) ? 'gallery-showcase-loading' : ''}`}
              onClick={() => handleImageClick(image.image_url || image.image)}
            >
              <img
                src={image.image_url || image.image}
                alt=""
                loading="lazy"
                onLoad={() => handleImageLoad(image.id)}
                onError={() => handleImageLoad(image.id)}
              />
            </div>
          ))}

          {/* Hide Button - Now at the end after all images */}
          <div className="gallery-showcase-hide-btn-container">
            <button
              id="gallery-showcase-hide-btn"
              className="gallery-showcase-btn gallery-showcase-secondary gallery-showcase-small-btn"
              onClick={handleHide}
            >
              Hide
            </button>
          </div>
        </div>
      )}
    </section>
  );
};

export default GallerySection;