import React from 'react';
import styled from 'styled-components';
import { FiDatabase } from 'react-icons/fi';

const HeaderContainer = styled.header`
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  color: white;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const HeaderContent = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1.5rem;
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.2rem;
`;

const LogoIcon = styled(FiDatabase)`
  font-size: 2.5rem;
  color: white;
`;

const HeaderText = styled.div`
  flex: 1;
`;

const Title = styled.h1`
  font-size: 2rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: -0.5px;
  
  @media (max-width: 768px) {
    font-size: 1.5rem;
  }
`;

const Subtitle = styled.p`
  font-size: 1rem;
  opacity: 0.95;
  margin: 0.25rem 0 0 0;
  font-weight: 400;
  
  @media (max-width: 768px) {
    font-size: 0.875rem;
  }
`;

const Header = () => {
  return (
    <HeaderContainer>
      <HeaderContent>
        <Logo>
          <LogoIcon />
        </Logo>
        <HeaderText>
          <Title>Tonkin Knowledge Finder</Title>
          <Subtitle>AI-Powered Project Intelligence & Expertise Discovery</Subtitle>
        </HeaderText>
      </HeaderContent>
    </HeaderContainer>
  );
};

export default Header;

