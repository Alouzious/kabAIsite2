import React from 'react';
import IndabaxNavbar from '../components/indabax/IndabaxNavbar';
import '../components/indabax/IndabaxNavbar.css';
import IndabaxFooter from '../components/layout/IndabaxFooter';
import '../components/layout/IndabaxFooter.css';
import HeroSection from '../components/indabax/HeroSection';
import LeadersSection from '../components/indabax/LeadersSection';
import IndabaxGallerySection from '../components/indabax/IndabaxGallerySection';
import LearningResourcesSection from '../components/indabax/LearningResourcesSection';
import '../components/indabax/LearningResourcesSection.css';
import IndabaxAboutSection from '../components/indabax/IndabaxAboutSection';
import '../components/indabax/IndabaxHero.css';
import '../components/indabax/LeadersSection.css';


const IndabaxHome = () => (
  <div>
    <IndabaxNavbar />
    <div id="hero"><HeroSection /></div>
    <div id="about"><IndabaxAboutSection /></div>
    <div id="leaders"><LeadersSection /></div>
    <div id="gallery"><IndabaxGallerySection /></div>
    <div id="resources"><LearningResourcesSection /></div>
    <IndabaxFooter />
  </div>
);

export default IndabaxHome;
