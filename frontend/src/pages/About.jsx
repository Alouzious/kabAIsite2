import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import Footer from '../components/layout/Footer';
import { sampleSiteSettings, sampleContactInfo } from '../data/sampleData';
import './About.css';

const About = () => {
  const [aboutData, setAboutData] = useState(null);
  const [siteSettings, setSiteSettings] = useState({});
  const [contactInfo, setContactInfo] = useState({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Fetch about data and site settings from API
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // TODO: Replace with actual API calls when Django backend is ready
      // const aboutResponse = await fetch(`${process.env.REACT_APP_API_BASE_URL}/about/`);
      // const aboutData = await aboutResponse.json();
      // setAboutData(aboutData);

      // For now, using sample data
      setSiteSettings(sampleSiteSettings);
      setContactInfo(sampleContactInfo);
      setAboutData(getDefaultAboutData());
    } catch (error) {
      console.error('Error fetching data:', error);
      // Use default data if API fails
      setSiteSettings(sampleSiteSettings);
      setContactInfo(sampleContactInfo);
      setAboutData(getDefaultAboutData());
    } finally {
      setLoading(false);
    }
  };

  const getDefaultAboutData = () => ({
    title: 'About KUAI Club',
    content:  'Empowering the future through artificial intelligence education and innovation. We are building Uganda\'s next generation of AI leaders and innovators.',
    hero_stat_1_value:  '500+',
    hero_stat_1_label: 'Students',
    hero_stat_2_value: '50+',
    hero_stat_2_label: 'Projects',
    hero_stat_3_value:  '15+',
    hero_stat_3_label: 'Partners',
    hero_stat_4_value: '3',
    hero_stat_4_label: 'Years',
    who_we_are_title: 'Who We Are',
    who_we_are_description: 'We are a diverse group passionate about exploring the frontiers of artificial intelligence.  Our club fosters collaboration among students, professionals, and researchers to learn, innovate, and create AI-driven solutions that address societal challenges.\n\nFrom machine learning enthusiasts to data science experts, our community brings together minds from various backgrounds united by a common vision of leveraging AI for positive impact.',
    who_we_are_image: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600',
    why_exist_title: 'Why We Exist',
    why_exist_description: 'We exist to inspire and equip members with the tools and expertise needed to navigate the rapidly evolving AI landscape. By fostering collaboration and continuous learning, we aim to accelerate AI innovation and create meaningful solutions.\n\nIn a world where artificial intelligence is reshaping industries and societies, we believe in democratizing AI knowledge and making it accessible to everyone, regardless of their background or experience level.',
    image: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600',
    mission: 'To democratize artificial intelligence education and foster innovation through collaborative learning, practical application, and community engagement. We strive to bridge the gap between theoretical knowledge and real-world AI solutions.',
    vision: 'To be the leading AI education and innovation hub in East Africa, producing world-class AI professionals who drive technological advancement and create solutions that benefit society and improve lives globally.',
    impact_subtitle: 'Making a difference in AI education and technology advancement in Uganda',
    impact_stat_1_value:  '1000+',
    impact_stat_1_label: 'Students Empowered',
    impact_stat_2_value: '75+',
    impact_stat_2_label: 'AI Projects Completed',
    impact_stat_3_value:  '25+',
    impact_stat_3_label: 'Partner Organizations',
    impact_stat_4_value: '5',
    impact_stat_4_label: 'Years of Innovation',
    cta_title: 'Ready to Join the AI Revolution? ',
    cta_description:  'Discover how KUAI Club can help you unlock the potential of artificial intelligence and transform your future through cutting-edge education and innovative solutions. Join our community of learners, innovators, and AI enthusiasts today.',
    cta_primary_text:  'Get Started Today',
    cta_primary_link: '/',
    cta_secondary_text: 'Explore Programs',
    cta_secondary_link: '/#projects-section'
  });

  // Intersection Observer for animations
  useEffect(() => {
    if (loading) return;

    const observerOptions = {
      threshold: 0.3,
      rootMargin:  '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, observerOptions);

    document.querySelectorAll('.section-card, .mvv-card, .stat-item').forEach(el => {
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, [loading]);

  // Counter animation
  useEffect(() => {
    if (loading) return;

    const animateCounter = (element, target, duration = 2000) => {
      let startTime = null;
      const startValue = 0;

      function animate(currentTime) {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / duration, 1);

        const currentValue = Math.floor(progress * target);
        element.textContent = currentValue + (target >= 1000 ? '+' :  '');

        if (progress < 1) {
          requestAnimationFrame(animate);
        }
      }

      requestAnimationFrame(animate);
    };

    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry. isIntersecting) {
          const target = entry.target;
          const text = target.textContent;
          const number = parseInt(text.replace(/\D/g, ''));

          if (number > 0) {
            animateCounter(target, number);
            counterObserver.unobserve(target);
          }
        }
      });
    }, { threshold: 0.5 });

    document.querySelectorAll('.stat-number, .hero-stat-number').forEach(el => {
      counterObserver. observe(el);
    });

    return () => counterObserver. disconnect();
  }, [loading]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  const about = aboutData;

  return (
    <div className="about-page">
      <Navbar siteSettings={siteSettings} />

      {/* Hero Section */}
      <div className="about-hero">
        <div className="container">
          <div className="hero-content">
            <h1>{about.title}</h1>
            <p className="hero-subtitle">{about.content}</p>
            <div className="hero-stats">
              <div className="hero-stat">
                <span className="hero-stat-number">{about.hero_stat_1_value}</span>
                <span className="hero-stat-label">{about.hero_stat_1_label}</span>
              </div>
              <div className="hero-stat">
                <span className="hero-stat-number">{about.hero_stat_2_value}</span>
                <span className="hero-stat-label">{about. hero_stat_2_label}</span>
              </div>
              <div className="hero-stat">
                <span className="hero-stat-number">{about. hero_stat_3_value}</span>
                <span className="hero-stat-label">{about.hero_stat_3_label}</span>
              </div>
              <div className="hero-stat">
                <span className="hero-stat-number">{about.hero_stat_4_value}</span>
                <span className="hero-stat-label">{about.hero_stat_4_label}</span>
              </div>
            </div>
          </div>
          <div className="scroll-indicator"></div>
        </div>
      </div>

      {/* Main Content */}
      <div className="about-content">
        <div className="container">
          {/* Who We Are & Why We Exist */}
          <div className="dual-section" id="who-we-are">
            {/* Who We Are */}
            <div className="section-card">
              <h2>{about.who_we_are_title}</h2>
              <p>{about. who_we_are_description}</p>
              {about.who_we_are_image && (
                <div className="section-image">
                  <img src={about.who_we_are_image} alt={about.who_we_are_title} loading="lazy" />
                </div>
              )}
            </div>

            {/* Why We Exist */}
            <div className="section-card">
              <h2>{about.why_exist_title}</h2>
              <p>{about.why_exist_description}</p>
              {about.image && (
                <div className="section-image">
                  <img src={about. image} alt={about.why_exist_title} loading="lazy" />
                </div>
              )}
            </div>
          </div>

          {/* Mission, Vision, Objectives */}
          <div className="foundation-section">
            <div className="section-header">
              <h2 className="section-title">Our Foundation</h2>
              <p className="section-subtitle">
                The core principles that drive everything we do at KUAI Club
              </p>
            </div>

            <div className="mvv-grid" id="mission">
              {/* Mission */}
              <div className="mvv-card">
                <div className="mvv-icon">
                  <svg fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
                  </svg>
                </div>
                <h3>Our Mission</h3>
                <p>{about.mission}</p>
              </div>

              {/* Vision */}
              <div className="mvv-card" id="vision">
                <div className="mvv-icon">
                  <svg fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                    <path fillRule="evenodd" d="M. 458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
                  </svg>
                </div>
                <h3>Our Vision</h3>
                <p>{about.vision}</p>
              </div>
            </div>
          </div>

          {/* Impact Section */}
          <div className="impact-section" id="impact">
            <div className="container">
              <div className="section-header">
                <h2 className="section-title" style={{ color: '#2c3e50' }}>Our Impact</h2>
                <p className="section-subtitle">{about.impact_subtitle}</p>
              </div>
              <div className="stats-grid">
                <div className="stat-item">
                  <span className="stat-number">{about.impact_stat_1_value}</span>
                  <div className="stat-label">{about.impact_stat_1_label}</div>
                </div>
                <div className="stat-item">
                  <span className="stat-number">{about.impact_stat_2_value}</span>
                  <div className="stat-label">{about.impact_stat_2_label}</div>
                </div>
                <div className="stat-item">
                  <span className="stat-number">{about.impact_stat_3_value}</span>
                  <div className="stat-label">{about.impact_stat_3_label}</div>
                </div>
                <div className="stat-item">
                  <span className="stat-number">{about. impact_stat_4_value}</span>
                  <div className="stat-label">{about. impact_stat_4_label}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="cta-section">
        <div className="container">
          <div className="cta-content">
            <h2 className="cta-title">{about.cta_title}</h2>
            <p className="cta-description">{about.cta_description}</p>
            <div className="cta-buttons">
              <a href={about.cta_primary_link} className="btn-primary">{about.cta_primary_text}</a>
              <a href={about. cta_secondary_link} className="btn-secondary">{about. cta_secondary_text}</a>
            </div>
          </div>
        </div>
      </div>

      <Footer siteSettings={siteSettings} contactInfo={contactInfo} />
    </div>
  );
};

export default About;