import React from 'react';
import styled from 'styled-components';
import { 
  FiX, 
  FiMail, 
  FiMessageSquare, 
  FiBriefcase,
  FiAward,
  FiTrendingUp 
} from 'react-icons/fi';
import { motion, AnimatePresence } from 'framer-motion';

const Overlay = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  overflow-y: auto;
`;

const Modal = styled(motion.div)`
  background: white;
  border-radius: 20px;
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  position: relative;
  
  @media (max-width: 768px) {
    margin: 1rem;
    max-height: calc(100vh - 2rem);
  }
`;

const CloseButton = styled.button`
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: #F1F5F9;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #64748B;
  z-index: 10;
  
  &:hover {
    background: #E2E8F0;
    color: #0F172A;
    transform: rotate(90deg);
  }
`;

const Header = styled.div`
  padding: 2.5rem 2.5rem 2rem 2.5rem;
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  color: white;
  border-radius: 20px 20px 0 0;
`;

const ExpertAvatarLarge = styled.div`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: white;
  color: #3B82F6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  border: 4px solid rgba(255, 255, 255, 0.3);
`;

const ExpertName = styled.h2`
  font-size: 2rem;
  font-weight: 800;
  margin: 0 0 0.5rem 0;
`;

const ExpertRole = styled.p`
  font-size: 1.125rem;
  opacity: 0.95;
  margin: 0;
  font-weight: 500;
`;

const Content = styled.div`
  padding: 2rem 2.5rem 2.5rem 2.5rem;
`;

const Section = styled.div`
  margin-bottom: 2rem;
  
  &:last-child {
    margin-bottom: 0;
  }
`;

const SectionHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
`;

const SectionIcon = styled.div`
  font-size: 1.25rem;
  color: #3B82F6;
`;

const SectionTitle = styled.h3`
  font-size: 1.125rem;
  font-weight: 700;
  color: #0F172A;
  margin: 0;
`;

const ContactButtons = styled.div`
  display: flex;
  gap: 1rem;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const ContactButton = styled.a`
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: ${props => props.primary ? '#3B82F6' : '#F1F5F9'};
  color: ${props => props.primary ? 'white' : '#475569'};
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
  
  &:hover {
    background: ${props => props.primary ? '#2563EB' : '#E2E8F0'};
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const StatCard = styled.div`
  padding: 1.25rem;
  background: #F8FAFC;
  border-radius: 12px;
  text-align: center;
  border: 1px solid #E2E8F0;
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: 700;
  color: #3B82F6;
  margin-bottom: 0.25rem;
`;

const StatLabel = styled.div`
  font-size: 0.875rem;
  color: #64748B;
  font-weight: 500;
`;

const ExpertiseTags = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
`;

const ExpertiseTag = styled.span`
  padding: 0.625rem 1.125rem;
  background: #EFF6FF;
  color: #1E40AF;
  border-radius: 20px;
  font-size: 0.95rem;
  font-weight: 500;
  border: 1px solid #DBEAFE;
`;

const ProjectsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
`;

const ProjectItem = styled.div`
  padding: 1rem;
  background: #F8FAFC;
  border-left: 3px solid #3B82F6;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #475569;
  transition: all 0.2s ease;
  
  &:hover {
    background: #F1F5F9;
    transform: translateX(4px);
  }
`;

const ProjectNumber = styled.span`
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
  font-weight: 600;
  color: #3B82F6;
  margin-right: 0.5rem;
`;

const ProjectName = styled.span`
  color: #0F172A;
  font-weight: 500;
`;

const ExpertFinder = ({ expert, onClose, projects }) => {
  if (!expert) return null;

  return (
    <AnimatePresence>
      <Overlay
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      >
        <Modal
          initial={{ opacity: 0, y: 50, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 50, scale: 0.95 }}
          transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          onClick={(e) => e.stopPropagation()}
        >
          <CloseButton onClick={onClose}>
            <FiX size={20} />
          </CloseButton>
          
          <Header>
            <ExpertAvatarLarge>{expert.avatar}</ExpertAvatarLarge>
            <ExpertName>{expert.name}</ExpertName>
            <ExpertRole>{expert.role}</ExpertRole>
          </Header>
          
          <Content>
            <Section>
              <SectionHeader>
                <SectionIcon><FiMail /></SectionIcon>
                <SectionTitle>Contact</SectionTitle>
              </SectionHeader>
              <ContactButtons>
                <ContactButton href={`mailto:${expert.email}`} primary>
                  <FiMail /> Email
                </ContactButton>
                <ContactButton href={`slack://user?team=tonkin&id=${expert.slack}`}>
                  <FiMessageSquare /> Slack
                </ContactButton>
              </ContactButtons>
            </Section>
            
            <Section>
              <SectionHeader>
                <SectionIcon><FiTrendingUp /></SectionIcon>
                <SectionTitle>Performance</SectionTitle>
              </SectionHeader>
              <StatsGrid>
                <StatCard>
                  <StatValue>{expert.projectsLed}</StatValue>
                  <StatLabel>Projects Led</StatLabel>
                </StatCard>
                <StatCard>
                  <StatValue>{expert.projectsReviewed}</StatValue>
                  <StatLabel>Reviews</StatLabel>
                </StatCard>
                <StatCard>
                  <StatValue>{(expert.avgTrustScore * 100).toFixed(0)}%</StatValue>
                  <StatLabel>Avg Trust Score</StatLabel>
                </StatCard>
              </StatsGrid>
            </Section>
            
            <Section>
              <SectionHeader>
                <SectionIcon><FiAward /></SectionIcon>
                <SectionTitle>Expertise</SectionTitle>
              </SectionHeader>
              <ExpertiseTags>
                {expert.expertise.map(skill => (
                  <ExpertiseTag key={skill}>{skill}</ExpertiseTag>
                ))}
              </ExpertiseTags>
            </Section>
            
            <Section>
              <SectionHeader>
                <SectionIcon><FiBriefcase /></SectionIcon>
                <SectionTitle>Recent Projects</SectionTitle>
              </SectionHeader>
              <ProjectsList>
                {projects.slice(0, 5).map(project => (
                  <ProjectItem key={project.id}>
                    <ProjectNumber>{project.projectNumber}</ProjectNumber>
                    <ProjectName>{project.projectName}</ProjectName>
                  </ProjectItem>
                ))}
              </ProjectsList>
            </Section>
          </Content>
        </Modal>
      </Overlay>
    </AnimatePresence>
  );
};

export default ExpertFinder;

