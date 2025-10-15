import React, { useState } from 'react';
import styled from 'styled-components';
import { FiSliders, FiUser } from 'react-icons/fi';
import { categories, regions } from '../data/sampleData';

const PanelContainer = styled.div`
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #E2E8F0;
  height: fit-content;
  position: sticky;
  top: 2rem;
  
  @media (max-width: 1024px) {
    position: relative;
    top: 0;
  }
`;

const PanelHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #F1F5F9;
`;

const PanelIcon = styled(FiSliders)`
  font-size: 1.25rem;
  color: #3B82F6;
`;

const PanelTitle = styled.h3`
  font-size: 1.125rem;
  font-weight: 700;
  color: #0F172A;
  margin: 0;
`;

const FilterSection = styled.div`
  margin-bottom: 1.5rem;
  
  &:last-child {
    margin-bottom: 0;
  }
`;

const FilterLabel = styled.label`
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const Slider = styled.input`
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(to right, 
    #EF4444 0%, 
    #F59E0B 25%, 
    #10B981 50%, 
    #3B82F6 100%
  );
  outline: none;
  -webkit-appearance: none;
  
  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #3B82F6;
    cursor: pointer;
    border: 3px solid white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
  
  &::-moz-range-thumb {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #3B82F6;
    cursor: pointer;
    border: 3px solid white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
`;

const SliderValue = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
`;

const CurrentValue = styled.span`
  font-size: 1rem;
  font-weight: 700;
  color: #3B82F6;
`;

const ValueLabel = styled.span`
  font-size: 0.75rem;
  color: #64748B;
`;

const CheckboxGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 200px;
  overflow-y: auto;
  padding-right: 0.5rem;
  
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: #F1F5F9;
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #CBD5E1;
    border-radius: 3px;
  }
`;

const CheckboxLabel = styled.label`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #475569;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  
  &:hover {
    background: #F8FAFC;
  }
  
  input {
    width: 16px;
    height: 16px;
    cursor: pointer;
    accent-color: #3B82F6;
  }
`;

const ExpertList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const ExpertButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  font-family: 'Inter', sans-serif;
  
  &:hover {
    background: #3B82F6;
    border-color: #3B82F6;
    transform: translateX(4px);
    
    span {
      color: white;
    }
  }
`;

const ExpertAvatar = styled.div`
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  flex-shrink: 0;
`;

const ExpertName = styled.span`
  font-size: 0.875rem;
  color: #475569;
  font-weight: 500;
  transition: color 0.2s ease;
`;

const ClearButton = styled.button`
  width: 100%;
  padding: 0.75rem;
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 1rem;
  font-family: 'Inter', sans-serif;
  
  &:hover {
    background: #E2E8F0;
    color: #0F172A;
  }
`;

const FilterPanel = ({ filters, onFilterChange, experts, onExpertSelect }) => {
  const handleTrustScoreChange = (e) => {
    onFilterChange({
      ...filters,
      minTrustScore: parseFloat(e.target.value)
    });
  };

  const handleCategoryChange = (category) => {
    const newCategories = filters.categories.includes(category)
      ? filters.categories.filter(c => c !== category)
      : [...filters.categories, category];
    
    onFilterChange({
      ...filters,
      categories: newCategories
    });
  };

  const handleRegionChange = (region) => {
    const newRegions = filters.regions.includes(region)
      ? filters.regions.filter(r => r !== region)
      : [...filters.regions, region];
    
    onFilterChange({
      ...filters,
      regions: newRegions
    });
  };

  const handleClearFilters = () => {
    onFilterChange({
      minTrustScore: 0,
      categories: [],
      regions: [],
      experts: []
    });
  };

  const hasActiveFilters = 
    filters.minTrustScore > 0 ||
    filters.categories.length > 0 ||
    filters.regions.length > 0 ||
    filters.experts.length > 0;

  return (
    <PanelContainer>
      <PanelHeader>
        <PanelIcon />
        <PanelTitle>Filters</PanelTitle>
      </PanelHeader>
      
      <FilterSection>
        <FilterLabel>Minimum Trust Score</FilterLabel>
        <Slider
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={filters.minTrustScore}
          onChange={handleTrustScoreChange}
        />
        <SliderValue>
          <CurrentValue>{(filters.minTrustScore * 100).toFixed(0)}%</CurrentValue>
          <ValueLabel>Quality Threshold</ValueLabel>
        </SliderValue>
      </FilterSection>
      
      <FilterSection>
        <FilterLabel>Categories</FilterLabel>
        <CheckboxGroup>
          {categories.map(category => (
            <CheckboxLabel key={category}>
              <input
                type="checkbox"
                checked={filters.categories.includes(category)}
                onChange={() => handleCategoryChange(category)}
              />
              {category}
            </CheckboxLabel>
          ))}
        </CheckboxGroup>
      </FilterSection>
      
      <FilterSection>
        <FilterLabel>Regions</FilterLabel>
        <CheckboxGroup>
          {regions.map(region => (
            <CheckboxLabel key={region}>
              <input
                type="checkbox"
                checked={filters.regions.includes(region)}
                onChange={() => handleRegionChange(region)}
              />
              {region}
            </CheckboxLabel>
          ))}
        </CheckboxGroup>
      </FilterSection>
      
      <FilterSection>
        <FilterLabel>
          <FiUser style={{ display: 'inline', marginRight: '0.5rem' }} />
          Find Experts
        </FilterLabel>
        <ExpertList>
          {experts.slice(0, 5).map(expert => (
            <ExpertButton 
              key={expert.name}
              onClick={() => onExpertSelect(expert.name)}
            >
              <ExpertAvatar>{expert.avatar}</ExpertAvatar>
              <ExpertName>{expert.name}</ExpertName>
            </ExpertButton>
          ))}
        </ExpertList>
      </FilterSection>
      
      {hasActiveFilters && (
        <ClearButton onClick={handleClearFilters}>
          Clear All Filters
        </ClearButton>
      )}
    </PanelContainer>
  );
};

export default FilterPanel;

