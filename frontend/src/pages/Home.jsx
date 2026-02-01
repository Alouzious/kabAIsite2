import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SEO from '../components/layout/SEO';
import Navbar from '../components/layout/Navbar';
import HeroSlider from '../components/home/HeroSlider';
import ProjectsSection from '../components/home/ProjectsSection';
import EventsSection from '../components/home/EventsSection';
import TeamSection from '../components/home/TeamSection';
import NewsSection from '../components/home/NewsSection';
import GallerySection from '../components/home/GallerySection';
import Footer from '../components/layout/Footer';
import PartnersSection from '../components/home/PartnersSection';

import './Home.css';
import config from '../api/config';

const siteName = process.env.REACT_APP_SITE_NAME || 'KUAI Club';
const siteDescription =
  process.env.REACT_APP_SITE_DESCRIPTION ||
  'Kabale University AI Club - Empowering the next generation of AI leaders in Uganda.';
const siteKeywords =
  process.env.REACT_APP_SITE_KEYWORDS ||
  'AI, Artificial Intelligence, Uganda, Kabale University, Machine Learning, Data Science';
const siteUrl = process.env.REACT_APP_SITE_URL || 'http://localhost:3000';

const Home = () => {
  const [siteSettings, setSiteSettings] = useState({});
  const [aboutPages, setAboutPages] = useState([]);
  const [news, setNews] = useState([]);
  const [events, setEvents] = useState([]);
  const [leaders, setLeaders] = useState([]);
  const [gallery, setGallery] = useState([]);
  // COMMENTED OUT - Not needed right now
  // const [research, setResearch] = useState([]);
  // const [resources, setResources] = useState([]);
  // const [community, setCommunity] = useState([]);
  const [projects, setProjects] = useState([]);
  const [contactInfo, setContactInfo] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Site settings
        const siteSettingsRes = await axios.get(`${config.API_BASE_URL}/core/site-settings/`);
        setSiteSettings(Array.isArray(siteSettingsRes.data) ? siteSettingsRes.data[0] : siteSettingsRes.data || {});

        // Contact Info
        const contactInfoRes = await axios.get(`${config.API_BASE_URL}/core/contact-info/`);
        setContactInfo(Array.isArray(contactInfoRes.data) ? contactInfoRes.data[0] : contactInfoRes.data || {});

        // About pages (if you have such an endpoint)
        const aboutPagesRes = await axios.get(`${config.API_BASE_URL}/about/`);
        setAboutPages(aboutPagesRes.data.results || aboutPagesRes.data || []);

        // News
        const newsRes = await axios.get(`${config.API_BASE_URL}/news/articles/`);
        setNews(newsRes.data.results || newsRes.data || []);

        // Events
        const eventsRes = await axios.get(`${config.API_BASE_URL}/events/`);
        setEvents(eventsRes.data.results || eventsRes.data || []);

        // Team leaders
        const leadersRes = await axios.get(`${config.API_BASE_URL}/team/members/`);
        setLeaders(leadersRes.data.results || leadersRes.data || []);

        // COMMENTED OUT - These endpoints don't exist yet
        // Uncomment when you create these endpoints in Django backend
        
        // // Research
        // const researchRes = await axios.get(`${config.API_BASE_URL}/research/`);
        // setResearch(researchRes.data.results || researchRes.data || []);

        // // Resources
        // const resourcesRes = await axios.get(`${config.API_BASE_URL}/resources/`);
        // setResources(resourcesRes.data.results || resourcesRes.data || []);

        // // Community
        // const communityRes = await axios.get(`${config.API_BASE_URL}/community/`);
        // setCommunity(communityRes.data.results || communityRes.data || []);

        // Projects
        const projectsRes = await axios.get(`${config.API_BASE_URL}/projects/`);
        setProjects(projectsRes.data.results || projectsRes.data || []);

        // Gallery
        const galleryRes = await axios.get(`${config.API_BASE_URL}/gallery/images/`);
        setGallery(galleryRes.data.results || galleryRes.data || []);

        setLoading(false);
      } catch (error) {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <>
      <SEO
        title={`${siteName} | Home`}
        description={siteDescription}
        keywords={siteKeywords}
        canonical={siteUrl}
      />

      <div className="home-page">
        <Navbar />

        <HeroSlider />

        <ProjectsSection />

        <EventsSection
          initialPastEvents={events.filter(e => e.type === 'past')}
          initialUpcomingEvents={events.filter(e => e.type === 'upcoming')}
          backgroundImage="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200"
        />

        <TeamSection initialLeaders={leaders} />
        <NewsSection initialNews={news} />
        <GallerySection initialGallery={gallery} />
        <PartnersSection />
        <Footer siteSettings={siteSettings} contactInfo={contactInfo} />
      </div>
    </>
  );
};

export default Home;