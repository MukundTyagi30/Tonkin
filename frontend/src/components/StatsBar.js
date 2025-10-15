import React from 'react';
import styled from 'styled-components';
import { FiCheckCircle, FiDatabase } from 'react-icons/fi';
import { motion } from 'framer-motion';

const StatsContainer = styled(motion.div)`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: white;
  border-radius: 12px;
  margin-top: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #E2E8F0;
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
`;

const StatItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const StatIcon = styled.div`
  font-size: 1.5rem;
  color: ${props => props.color || '#3B82F6'};
`;

const StatContent = styled.div`
  display: flex;
  flex-direction: column;
`;

const StatValue = styled.span`
  font-size: 1.25rem;
  font-weight: 700;
  color: #0F172A;
`;

const StatLabel = styled.span`
  font-size: 0.875rem;
  color: #64748B;
  font-weight: 500;
`;

const QueryText = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  color: #475569;
  
  @media (max-width: 768px) {
    width: 100%;
  }
`;

const QueryLabel = styled.span`
  font-weight: 500;
`;

const QueryValue = styled.span`
  font-weight: 700;
  color: #3B82F6;
`;

const StatsBar = ({ resultCount, totalProjects, searchQuery }) => {
  return (
    <StatsContainer
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <StatItem>
        <StatIcon color="#10B981">
          <FiCheckCircle />
        </StatIcon>
        <StatContent>
          <StatValue>{resultCount}</StatValue>
          <StatLabel>Results Found</StatLabel>
        </StatContent>
      </StatItem>
      
      <QueryText>
        <QueryLabel>Searching for:</QueryLabel>
        <QueryValue>"{searchQuery}"</QueryValue>
      </QueryText>
      
      <StatItem>
        <StatIcon color="#64748B">
          <FiDatabase />
        </StatIcon>
        <StatContent>
          <StatValue>{totalProjects}</StatValue>
          <StatLabel>Indexed Projects</StatLabel>
        </StatContent>
      </StatItem>
    </StatsContainer>
  );
};

export default StatsBar;

