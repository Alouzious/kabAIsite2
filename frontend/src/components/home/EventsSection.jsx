import React, { useState, useEffect, useRef } from 'react';
import './EventsSection.css';
import config from "../../api/config";

const EventsSection = ({ backgroundImage = '' }) => {
  const [pastEvents, setPastEvents] = useState({
    events: [],
    page: 1,
    totalPages: 1,
    loading: true
  });

  const [upcomingEvents, setUpcomingEvents] = useState({
    events: [],
    page: 1,
    totalPages: 1,
    loading: true
  });

  const countdownInterval = useRef(null);

  // Fetch events from API and split into past/upcoming
  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch(`${config.API_BASE_URL}/events/`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const events = data.results || data || [];
        
        // Ensure events is an array before filtering
        const eventsArray = Array.isArray(events) ? events : [];
        
        // Split into past & upcoming using API fields
        const upcoming = eventsArray.filter(ev => ev.is_upcoming);
        const past = eventsArray.filter(ev => ev.is_past);
        
        setUpcomingEvents({
          events: upcoming,
          page: 1,
          totalPages: 1,
          loading: false
        });
        setPastEvents({
          events: past,
          page: 1,
          totalPages: 1,
          loading: false
        });
      } catch (error) {
        console.error('Error loading events:', error);
        setUpcomingEvents(prev => ({ ...prev, loading: false }));
        setPastEvents(prev => ({ ...prev, loading: false }));
      }
    };

    fetchEvents();
  }, []);

  // Update countdown timers
  const updateCountdowns = () => {
    const countdownElements = document.querySelectorAll('.events-countdown-timer[data-start]');
    countdownElements.forEach(element => {
      const startDate = new Date(element.getAttribute('data-start'));
      const now = new Date();
      const timeDiff = startDate - now;
      if (timeDiff > 0) {
        const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
        const daysEl = element.querySelector('.events-timer-days');
        const hoursEl = element.querySelector('.events-timer-hours');
        const minutesEl = element.querySelector('.events-timer-minutes');
        if (daysEl) daysEl.textContent = days.toString().padStart(2, '0');
        if (hoursEl) hoursEl.textContent = hours.toString().padStart(2, '0');
        if (minutesEl) minutesEl.textContent = minutes.toString().padStart(2, '0');
      } else {
        element.innerHTML = '<div class="events-live-badge">🔴 LIVE NOW</div>';
      }
    });
  };

  useEffect(() => {
    updateCountdowns();
    countdownInterval.current = setInterval(updateCountdowns, 60000);

    return () => {
      if (countdownInterval.current) {
        clearInterval(countdownInterval.current);
      }
    };
  }, [upcomingEvents.events]);

  // Format date
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return {
      day: date.getDate(),
      month: date.toLocaleString('default', { month: 'short' }).toUpperCase(),
      year: date.getFullYear()
    };
  };

  // Featured Event Card (for upcoming - first event gets hero treatment)
  const FeaturedEventCard = ({ event }) => {
    const dateInfo = event.date ? formatDate(event.date) : null;

    return (
      <div className="events-featured-card">
        <div className="events-featured-image">
          <img
            src={event.image_thumbnail_url}
            alt={event.title}
            loading="lazy"
          />
          <div className="events-featured-badge">Featured Event</div>
          {dateInfo && (
            <div className="events-date-badge">
              <span className="events-date-day">{dateInfo.day}</span>
              <span className="events-date-month">{dateInfo.month}</span>
            </div>
          )}
        </div>
        <div className="events-featured-content">
          <h3 className="events-featured-title">{event.title}</h3>
          
          {event.description && (
            <p className="events-featured-summary">{event.description}</p>
          )}

          <div className="events-info-grid">
            <div className="events-info-item">
              <span className="events-info-icon">📅</span>
              <div className="events-info-text">
                <span className="events-info-label">Date & Time</span>
                <span className="events-info-value">
                  {event.date}
                  {event.time && ` • ${event.time}`}
                  {event.end_date && ` — ${event.end_date}`}
                </span>
              </div>
            </div>

            {event.location && (
              <div className="events-info-item">
                <span className="events-info-icon">📍</span>
                <div className="events-info-text">
                  <span className="events-info-label">Location</span>
                  <span className="events-info-value">{event.location}</span>
                </div>
              </div>
            )}

            {event.venue_details && (
              <div className="events-info-item">
                <span className="events-info-icon">🏛️</span>
                <div className="events-info-text">
                  <span className="events-info-label">Venue</span>
                  <span className="events-info-value">{event.venue_details}</span>
                </div>
              </div>
            )}

            {event.max_participants && (
              <div className="events-info-item">
                <span className="events-info-icon">👥</span>
                <div className="events-info-text">
                  <span className="events-info-label">Capacity</span>
                  <span className="events-info-value">{event.max_participants} participants</span>
                </div>
              </div>
            )}

            {event.registration_deadline && (
              <div className="events-info-item">
                <span className="events-info-icon">⏳</span>
                <div className="events-info-text">
                  <span className="events-info-label">Register By</span>
                  <span className="events-info-value">{event.registration_deadline}</span>
                </div>
              </div>
            )}
          </div>

          {event.date && event.is_upcoming && (
            <div className="events-countdown-timer" data-start={event.date + 'T' + (event.time || '00:00:00')}>
              <div className="events-countdown-label">Event Starts In:</div>
              <div className="events-countdown-digits">
                <div className="events-time-unit">
                  <span className="events-timer-days">00</span>
                  <span className="events-timer-label">Days</span>
                </div>
                <div className="events-time-unit">
                  <span className="events-timer-hours">00</span>
                  <span className="events-timer-label">Hours</span>
                </div>
                <div className="events-time-unit">
                  <span className="events-timer-minutes">00</span>
                  <span className="events-timer-label">Minutes</span>
                </div>
              </div>
            </div>
          )}

          {event.registration_link && (
            <a href={event.registration_link} target="_blank" rel="noopener noreferrer" className="events-featured-cta">
              Register Now
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M6 12L10 8L6 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </a>
          )}
        </div>
      </div>
    );
  };

  // Regular Event Card
  const EventCard = ({ event, showDate = false }) => {
    const dateInfo = event.date ? formatDate(event.date) : null;

    return (
      <div className="events-modern-card">
        <div className="events-card-image-wrapper">
          <img
            src={event.image_thumbnail_url}
            alt={event.title}
            loading="lazy"
          />
          {showDate && dateInfo && (
            <div className="events-date-badge-small">
              <span className="events-date-day-small">{dateInfo.day}</span>
              <span className="events-date-month-small">{dateInfo.month}</span>
            </div>
          )}
        </div>
        <div className="events-card-content">
          <h4 className="events-card-title">{event.title}</h4>
          
          {event.description && (
            <p className="events-card-description">{event.description}</p>
          )}

          <div className="events-card-details">
            <div className="events-card-detail-item">
              <span className="events-meta-icon">📅</span>
              <span className="events-meta-text">
                {event.date}
                {event.time && ` • ${event.time}`}
              </span>
            </div>

            {event.location && (
              <div className="events-card-detail-item">
                <span className="events-meta-icon">📍</span>
                <span className="events-meta-text">{event.location}</span>
              </div>
            )}

            {event.venue_details && (
              <div className="events-card-detail-item">
                <span className="events-meta-icon">🏛️</span>
                <span className="events-meta-text">{event.venue_details}</span>
              </div>
            )}
          </div>

          {event.registration_link && (
            <a href={event.registration_link} target="_blank" rel="noopener noreferrer" className="events-card-link">
              Learn More →
            </a>
          )}
        </div>
      </div>
    );
  };

  return (
    <section 
      id="events-section" 
      className="events-modern-section"
      style={{ backgroundImage: backgroundImage ? `url(${backgroundImage})` : 'none' }}
    >
      <div className="events-section-overlay"></div>
      <div className="events-wrapper">
        {/* Section Header */}
        <div className="events-section-header">
          <span className="events-section-subtitle">What's Happening</span>
          <h2 className="events-section-title">Events & Activities</h2>
          <p className="events-section-description">
            Stay updated with our latest events and past achievements
          </p>
        </div>

        {/* Upcoming Events */}
        <div className="events-block events-upcoming-block">
          <div className="events-block-header">
            <h3 className="events-block-title">
              <span className="events-title-icon">📅</span>
              Upcoming Events
            </h3>
          </div>
          {upcomingEvents.loading ? (
            <div className="events-loading-state">
              <div className="events-spinner"></div>
              <p>Loading events...</p>
            </div>
          ) : upcomingEvents.events.length > 0 ? (
            <>
              <FeaturedEventCard event={upcomingEvents.events[0]} />
              {upcomingEvents.events.length > 1 && (
                <div className="events-grid">
                  {upcomingEvents.events.slice(1).map(event => (
                    <EventCard key={event.id} event={event} showDate={true} />
                  ))}
                </div>
              )}
            </>
          ) : (
            <div className="events-empty-state">
              <div className="events-empty-icon">📭</div>
              <p>No upcoming events at the moment</p>
            </div>
          )}
        </div>

        {/* Past Events */}
        <div className="events-block events-past-block">
          <div className="events-block-header">
            <h3 className="events-block-title">
              <span className="events-title-icon">🏆</span>
              Past Events
            </h3>
          </div>
          {pastEvents.loading ? (
            <div className="events-loading-state">
              <div className="events-spinner"></div>
              <p>Loading events...</p>
            </div>
          ) : pastEvents.events.length > 0 ? (
            <div className="events-past-container">
              {pastEvents.events.map(event => (
                <EventCard key={event.id} event={event} showDate={true} />
              ))}
            </div>
          ) : (
            <div className="events-empty-state">
              <div className="events-empty-icon">📭</div>
              <p>No past events to display</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default EventsSection;