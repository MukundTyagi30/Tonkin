import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const BadgeContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  position: relative;
`;

const BadgeLabel = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const ScoreValue = styled.span`
  font-size: 1rem;
  font-weight: 700;
  color: ${props => props.color || '#3B82F6'};
`;

const ProgressBar = styled.div`
  width: 100%;
  height: 12px;
  background: #E2E8F0;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
  cursor: help;
`;

const ProgressFill = styled(motion.div)`
  height: 100%;
  background: ${props => {
    const percentage = props.percentage;
    if (percentage >= 90) return 'linear-gradient(90deg, #10B981 0%, #059669 100%)';
    if (percentage >= 75) return 'linear-gradient(90deg, #3B82F6 0%, #2563EB 100%)';
    if (percentage >= 60) return 'linear-gradient(90deg, #F59E0B 0%, #D97706 100%)';
    return 'linear-gradient(90deg, #EF4444 0%, #DC2626 100%)';
  }};
  border-radius: 6px;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.3),
      transparent
    );
    animation: shimmer 2s infinite;
  }
  
  @keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }
`;

const Tooltip = styled.div`
  position: absolute;
  bottom: calc(100% + 0.5rem);
  left: 50%;
  transform: translateX(-50%);
  background: #1E293B;
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  white-space: nowrap;
  z-index: 10;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  opacity: ${props => props.show ? 1 : 0};
  pointer-events: none;
  transition: opacity 0.2s ease;
  
  &::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent;
    border-top-color: #1E293B;
  }
`;

const TrustBadge = ({ score, label, tooltip, color }) => {
  const [showTooltip, setShowTooltip] = useState(false);
  const percentage = Math.round(score * 100);

  return (
    <BadgeContainer
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <BadgeLabel>
        <span>{label}</span>
        <ScoreValue color={color}>{percentage}%</ScoreValue>
      </BadgeLabel>
      
      <ProgressBar>
        <ProgressFill
          percentage={percentage}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
        />
      </ProgressBar>
      
      {tooltip && (
        <Tooltip show={showTooltip}>
          {tooltip}
        </Tooltip>
      )}
    </BadgeContainer>
  );
};

export default TrustBadge;

