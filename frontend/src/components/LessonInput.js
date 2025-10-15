import React, { useState } from 'react';
import styled from 'styled-components';
import { FiPlusCircle, FiCheck } from 'react-icons/fi';
import { motion, AnimatePresence } from 'framer-motion';

const InputContainer = styled.div`
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #E2E8F0;
`;

const InputHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
`;

const InputTitle = styled.h5`
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const InputWrapper = styled.div`
  display: flex;
  gap: 0.75rem;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const Input = styled.input`
  flex: 1;
  padding: 0.875rem 1rem;
  font-size: 0.95rem;
  border: 2px solid #E2E8F0;
  border-radius: 10px;
  background: #F8FAFC;
  color: #0F172A;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
  
  &:focus {
    outline: none;
    border-color: #3B82F6;
    background: white;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  &::placeholder {
    color: #94A3B8;
  }
`;

const SubmitButton = styled(motion.button)`
  padding: 0.875rem 1.5rem;
  background: ${props => props.disabled ? '#CBD5E1' : '#10B981'};
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: ${props => props.disabled ? 'not-allowed' : 'pointer'};
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Inter', sans-serif;
  transition: all 0.2s ease;
  white-space: nowrap;
  
  &:hover {
    background: ${props => props.disabled ? '#CBD5E1' : '#059669'};
    transform: ${props => props.disabled ? 'none' : 'translateY(-1px)'};
    box-shadow: ${props => props.disabled ? 'none' : '0 4px 12px rgba(16, 185, 129, 0.4)'};
  }
  
  @media (max-width: 768px) {
    width: 100%;
    justify-content: center;
  }
`;

const SuccessMessage = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1rem;
  background: #D1FAE5;
  color: #065F46;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 500;
  margin-top: 0.75rem;
`;

const LessonInput = ({ projectId, projectPhase, onSubmit }) => {
  const [lesson, setLesson] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const handleSubmit = async () => {
    if (!lesson.trim()) return;
    
    setIsSubmitting(true);
    
    const lessonData = {
      text: lesson,
      phase: projectPhase,
      author: 'Current User', // In production, get from auth
      date: new Date().toISOString(),
    };
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 500));
    
    onSubmit(projectId, lessonData);
    
    setLesson('');
    setIsSubmitting(false);
    setShowSuccess(true);
    
    setTimeout(() => {
      setShowSuccess(false);
    }, 3000);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <InputContainer>
      <InputHeader>
        <FiPlusCircle style={{ fontSize: '1rem', color: '#10B981' }} />
        <InputTitle>Add Lesson Learned / Decision</InputTitle>
      </InputHeader>
      
      <InputWrapper>
        <Input
          type="text"
          value={lesson}
          onChange={(e) => setLesson(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Share a key insight or decision from this project..."
          disabled={isSubmitting}
        />
        
        <SubmitButton
          onClick={handleSubmit}
          disabled={!lesson.trim() || isSubmitting}
          whileHover={{ scale: lesson.trim() ? 1.02 : 1 }}
          whileTap={{ scale: lesson.trim() ? 0.98 : 1 }}
        >
          <FiPlusCircle />
          {isSubmitting ? 'Saving...' : 'Add Lesson'}
        </SubmitButton>
      </InputWrapper>
      
      <AnimatePresence>
        {showSuccess && (
          <SuccessMessage
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <FiCheck style={{ fontSize: '1.25rem' }} />
            Lesson saved successfully! Tagged with {projectPhase} phase.
          </SuccessMessage>
        )}
      </AnimatePresence>
    </InputContainer>
  );
};

export default LessonInput;

