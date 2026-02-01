import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './IndabaxGallery.css';
import config from "../../api/config";

const IndabaxGallerySection = () => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    axios.get(`${config.API_BASE_URL}/indabax/gallery/`)
      .then(res => {
        setImages(res.data.results); // FIX: Access results array
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load gallery.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="gallery-loading">Loading gallery...</div>;
  if (error) return <div className="gallery-error">{error}</div>;
  if (!images.length) return <div className="gallery-empty">No gallery images found.</div>;

  const firstFourImages = images.slice(0, 4);
  const remainingImages = images.slice(4);
  const hasMoreImages = remainingImages.length > 0;

  return (
    <section className="indabax-gallery">
      <div className="container">
        <h2 className="gallery-title">Gallery</h2>
        
        {/* First 4 Images - Always Visible */}
        <div className="gallery-grid">
          {firstFourImages.map(img => (
            <div key={img.id} className="gallery-card">
              {img.image_thumbnail_url ? (
                <img src={img.image_thumbnail_url} alt={img.title} className="gallery-img" />
              ) : img.image_url ? (
                <img src={img.image_url} alt={img.title} className="gallery-img" />
              ) : (
                <div className="gallery-placeholder">No Image</div>
              )}
            </div>
          ))}
        </div>

        {/* Show More Button - Only when not expanded */}
        {hasMoreImages && !showAll && (
          <div className="gallery-button-wrapper">
            <button 
              className="gallery-toggle-btn"
              onClick={() => setShowAll(true)}
            >
              See More ({remainingImages.length} more)
            </button>
          </div>
        )}

        {/* Remaining Images - Show when expanded */}
        {hasMoreImages && showAll && (
          <div className="gallery-grid gallery-additional">
            {remainingImages.map(img => (
              <div key={img.id} className="gallery-card">
                {img.image_thumbnail_url ? (
                  <img src={img.image_thumbnail_url} alt={img.title} className="gallery-img" />
                ) : img.image_url ? (
                  <img src={img.image_url} alt={img.title} className="gallery-img" />
                ) : (
                  <div className="gallery-placeholder">No Image</div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Hide Button - Only when expanded, below all images */}
        {hasMoreImages && showAll && (
          <div className="gallery-button-wrapper">
            <button 
              className="gallery-toggle-btn"
              onClick={() => setShowAll(false)}
            >
              Hide
            </button>
          </div>
        )}
      </div>
    </section>
  );
};

export default IndabaxGallerySection;