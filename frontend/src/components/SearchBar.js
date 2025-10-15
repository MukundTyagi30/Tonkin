import React, { useState } from 'react';
import styled from 'styled-components';
import { FiSearch } from 'react-icons/fi';
import { motion } from 'framer-motion';

const SearchContainer = styled.div`
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  border: 1px solid #E2E8F0;
`;

const SearchInputWrapper = styled.div`
  position: relative;
  display: flex;
  gap: 1rem;
  align-items: center;
`;

const SearchIcon = styled(FiSearch)`
  position: absolute;
  left: 1.25rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.25rem;
  color: #94A3B8;
  pointer-events: none;
`;

const SearchInput = styled.input`
  flex: 1;
  padding: 1rem 1rem 1rem 3.5rem;
  font-size: 1rem;
  border: 2px solid #E2E8F0;
  border-radius: 12px;
  background: #F8FAFC;
  color: #0F172A;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  
  &:focus {
    outline: none;
    border-color: #3B82F6;
    background: white;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  &::placeholder {
    color: #94A3B8;
    font-weight: 400;
  }
`;

const SearchButton = styled(motion.button)`
  padding: 1rem 2rem;
  background: #3B82F6;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  font-family: 'Inter', sans-serif;
  
  &:hover {
    background: #2563EB;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  }
  
  &:active {
    transform: translateY(0);
  }
  
  @media (max-width: 768px) {
    padding: 1rem 1.5rem;
  }
`;

const RecentSearches = styled.div`
  margin-top: 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
`;

const RecentLabel = styled.span`
  font-size: 0.875rem;
  color: #64748B;
  font-weight: 500;
`;

const RecentTag = styled(motion.button)`
  padding: 0.5rem 1rem;
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  font-size: 0.875rem;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  
  &:hover {
    background: #3B82F6;
    color: white;
    border-color: #3B82F6;
    transform: translateY(-1px);
  }
`;

const SearchBar = ({ onSearch, recentSearches, totalProjects }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  const handleRecentClick = (searchText) => {
    setQuery(searchText);
    onSearch(searchText);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  return (
    <SearchContainer>
      <form onSubmit={handleSubmit}>
        <SearchInputWrapper>
          <SearchIcon />
          <SearchInput
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Search projects, documents, or expertise…"
            aria-label="Search"
          />
          <SearchButton
            type="submit"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            Search
          </SearchButton>
        </SearchInputWrapper>
      </form>
      
      {recentSearches.length > 0 && (
        <RecentSearches>
          <RecentLabel>Recent:</RecentLabel>
          {recentSearches.map((search, index) => (
            <RecentTag
              key={index}
              onClick={() => handleRecentClick(search)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {search}
            </RecentTag>
          ))}
        </RecentSearches>
      )}
    </SearchContainer>
  );
};

export default SearchBar;

