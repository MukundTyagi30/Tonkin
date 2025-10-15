import React, { useState } from 'react';
import styled from 'styled-components';
import { 
  FiThumbsUp, 
  FiThumbsDown, 
  FiUser, 
  FiMapPin, 
  FiCalendar,
  FiDollarSign,
  FiActivity,
  FiMessageSquare
} from 'react-icons/fi';
import TrustBadge from './TrustBadge';
import LessonInput from './LessonInput';

const Card = styled.div`
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 2px solid #E2E8F0;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 6px;
    height: 100%;
    background: linear-gradient(to bottom, #3B82F6, #10B981);
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
    border-color: #3B82F6;
    
    &::before {
      opacity: 1;
    }
  }
`;

const CardHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const HeaderContent = styled.div`
  flex: 1;
`;

const ProjectNumber = styled.div`
  font-size: 0.875rem;
  font-weight: 600;
  color: #3B82F6;
  margin-bottom: 0.5rem;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
`;

const ProjectTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 700;
  color: #0F172A;
  margin: 0 0 0.75rem 0;
  line-height: 1.3;
`;

const ProjectDescription = styled.p`
  font-size: 1rem;
  color: #475569;
  line-height: 1.6;
  margin: 0;
`;

const ScoresContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  min-width: 200px;
  
  @media (max-width: 768px) {
    width: 100%;
  }
`;

const MetadataGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1.5rem;
  background: #F8FAFC;
  border-radius: 12px;
  margin: 1.5rem 0;
  border: 1px solid #F1F5F9;
`;

const MetadataItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const MetadataIcon = styled.div`
  font-size: 1.25rem;
  color: #64748B;
`;

const MetadataContent = styled.div`
  display: flex;
  flex-direction: column;
`;

const MetadataLabel = styled.span`
  font-size: 0.75rem;
  color: #64748B;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const MetadataValue = styled.span`
  font-size: 0.95rem;
  color: #0F172A;
  font-weight: 600;
`;

const TagsContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1.5rem 0;
`;

const Tag = styled.span`
  padding: 0.4rem 0.9rem;
  background: #EFF6FF;
  color: #1E40AF;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid #DBEAFE;
`;

const DisciplineTag = styled(Tag)`
  background: #F0FDF4;
  color: #15803D;
  border-color: #D1FAE5;
`;

const ExpertsSection = styled.div`
  padding-top: 1.5rem;
  border-top: 1px solid #E2E8F0;
  margin-top: 1.5rem;
`;

const ExpertsHeader = styled.h4`
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  margin: 0 0 1rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const ExpertsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
`;

const ExpertCard = styled.button`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  font-family: 'Inter', sans-serif;
  
  &:hover {
    background: #3B82F6;
    border-color: #3B82F6;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
    
    div, span {
      color: white;
    }
  }
`;

const ExpertAvatar = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 700;
  flex-shrink: 0;
  transition: all 0.2s ease;
`;

const ExpertInfo = styled.div`
  display: flex;
  flex-direction: column;
  flex: 1;
`;

const ExpertName = styled.span`
  font-size: 0.95rem;
  font-weight: 600;
  color: #0F172A;
  transition: color 0.2s ease;
`;

const ExpertRole = styled.span`
  font-size: 0.8rem;
  color: #64748B;
  transition: color 0.2s ease;
`;

const LessonsSection = styled.div`
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #E2E8F0;
`;

const LessonsHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
`;

const LessonsTitle = styled.h4`
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const LessonsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
`;

const LessonItem = styled.div`
  padding: 1rem;
  background: #FFFBEB;
  border-left: 3px solid #F59E0B;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #475569;
  line-height: 1.5;
`;

const LessonMeta = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #92400E;
  font-weight: 500;
`;

const CardFooter = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #E2E8F0;
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
`;

const FeedbackButtons = styled.div`
  display: flex;
  gap: 0.75rem;
`;

const FeedbackButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: ${props => props.active ? '#3B82F6' : '#F1F5F9'};
  color: ${props => props.active ? 'white' : '#64748B'};
  border: 1px solid ${props => props.active ? '#3B82F6' : '#E2E8F0'};
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
  
  &:hover {
    background: ${props => props.active ? '#2563EB' : '#E2E8F0'};
    transform: translateY(-1px);
  }
`;

const StatusBadge = styled.div`
  padding: 0.5rem 1rem;
  background: ${props => {
    switch(props.status) {
      case 'Active': return '#D1FAE5';
      case 'Completed': return '#DBEAFE';
      case 'Planning': return '#FEF3C7';
      default: return '#F3F4F6';
    }
  }};
  color: ${props => {
    switch(props.status) {
      case 'Active': return '#065F46';
      case 'Completed': return '#1E40AF';
      case 'Planning': return '#92400E';
      default: return '#374151';
    }
  }};
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  
  @media (max-width: 768px) {
    align-self: flex-start;
  }
`;

const ResultCard = ({ project, onFeedback, onLessonSubmit, onExpertClick }) => {
  const [feedback, setFeedback] = useState(null);
  
  const handleFeedback = (isPositive) => {
    const newFeedback = feedback === isPositive ? null : isPositive;
    setFeedback(newFeedback);
    onFeedback(project.id, newFeedback);
  };

  // Generate expert initials from name
  const getInitials = (name) => {
    return name.split(' ').map(n => n[0]).join('');
  };

  return (
    <Card>
      <CardHeader>
        <HeaderContent>
          <ProjectNumber>{project.projectNumber}</ProjectNumber>
          <ProjectTitle>{project.projectName}</ProjectTitle>
          <ProjectDescription>{project.description}</ProjectDescription>
        </HeaderContent>
        
        <ScoresContainer>
          <TrustBadge 
            score={project.trustScore} 
            label="Trust Score"
            tooltip="Overall project quality and reliability score"
          />
          <TrustBadge 
            score={project.similarityScore} 
            label="Relevance"
            tooltip="How well this project matches your search"
            color="#10B981"
          />
        </ScoresContainer>
      </CardHeader>
      
      <MetadataGrid>
        <MetadataItem>
          <MetadataIcon><FiUser /></MetadataIcon>
          <MetadataContent>
            <MetadataLabel>Client</MetadataLabel>
            <MetadataValue>{project.client}</MetadataValue>
          </MetadataContent>
        </MetadataItem>
        
        <MetadataItem>
          <MetadataIcon><FiMapPin /></MetadataIcon>
          <MetadataContent>
            <MetadataLabel>Region</MetadataLabel>
            <MetadataValue>{project.region}</MetadataValue>
          </MetadataContent>
        </MetadataItem>
        
        <MetadataItem>
          <MetadataIcon><FiCalendar /></MetadataIcon>
          <MetadataContent>
            <MetadataLabel>Timeline</MetadataLabel>
            <MetadataValue>{project.phase}</MetadataValue>
          </MetadataContent>
        </MetadataItem>
        
        <MetadataItem>
          <MetadataIcon><FiDollarSign /></MetadataIcon>
          <MetadataContent>
            <MetadataLabel>Budget</MetadataLabel>
            <MetadataValue>{project.budget}</MetadataValue>
          </MetadataContent>
        </MetadataItem>
        
        <MetadataItem>
          <MetadataIcon><FiActivity /></MetadataIcon>
          <MetadataContent>
            <MetadataLabel>Category</MetadataLabel>
            <MetadataValue>{project.category}</MetadataValue>
          </MetadataContent>
        </MetadataItem>
      </MetadataGrid>
      
      <TagsContainer>
        {project.disciplines.map(discipline => (
          <DisciplineTag key={discipline}>{discipline}</DisciplineTag>
        ))}
        {project.tags.slice(0, 3).map(tag => (
          <Tag key={tag}>#{tag}</Tag>
        ))}
      </TagsContainer>
      
      <ExpertsSection>
        <ExpertsHeader>Project Team</ExpertsHeader>
        <ExpertsGrid>
          <ExpertCard onClick={() => onExpertClick(project.projectLeader)}>
            <ExpertAvatar>{getInitials(project.projectLeader)}</ExpertAvatar>
            <ExpertInfo>
              <ExpertName>{project.projectLeader}</ExpertName>
              <ExpertRole>Project Leader</ExpertRole>
            </ExpertInfo>
          </ExpertCard>
          
          {project.projectReviewer && (
            <ExpertCard onClick={() => onExpertClick(project.projectReviewer)}>
              <ExpertAvatar>{getInitials(project.projectReviewer)}</ExpertAvatar>
              <ExpertInfo>
                <ExpertName>{project.projectReviewer}</ExpertName>
                <ExpertRole>Reviewer</ExpertRole>
              </ExpertInfo>
            </ExpertCard>
          )}
        </ExpertsGrid>
      </ExpertsSection>
      
      {project.lessons && project.lessons.length > 0 && (
        <LessonsSection>
          <LessonsHeader>
            <FiMessageSquare style={{ fontSize: '1rem', color: '#F59E0B' }} />
            <LessonsTitle>Lessons Learned</LessonsTitle>
          </LessonsHeader>
          <LessonsList>
            {project.lessons.map(lesson => (
              <LessonItem key={lesson.id}>
                {lesson.text}
                <LessonMeta>
                  <span>{lesson.author}</span>
                  <span>•</span>
                  <span>{lesson.phase}</span>
                  <span>•</span>
                  <span>{new Date(lesson.date).toLocaleDateString()}</span>
                </LessonMeta>
              </LessonItem>
            ))}
          </LessonsList>
        </LessonsSection>
      )}
      
      <LessonInput 
        projectId={project.id}
        projectPhase={project.phase}
        onSubmit={onLessonSubmit}
      />
      
      <CardFooter>
        <FeedbackButtons>
          <FeedbackButton 
            active={feedback === true}
            onClick={() => handleFeedback(true)}
          >
            <FiThumbsUp /> Helpful
          </FeedbackButton>
          <FeedbackButton 
            active={feedback === false}
            onClick={() => handleFeedback(false)}
          >
            <FiThumbsDown /> Not Relevant
          </FeedbackButton>
        </FeedbackButtons>
        
        <StatusBadge status={project.status}>
          {project.status}
        </StatusBadge>
      </CardFooter>
    </Card>
  );
};

export default ResultCard;

