import React from 'react';
import styled from 'styled-components';
import ResultCard from './ResultCard';
import { motion } from 'framer-motion';

const ResultsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const ResultsList = ({ results, onFeedback, onLessonSubmit, onExpertClick }) => {
  return (
    <ResultsContainer>
      {results.map((result, index) => (
        <motion.div
          key={result.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: index * 0.1 }}
        >
          <ResultCard
            project={result}
            onFeedback={onFeedback}
            onLessonSubmit={onLessonSubmit}
            onExpertClick={onExpertClick}
          />
        </motion.div>
      ))}
    </ResultsContainer>
  );
};

export default ResultsList;

