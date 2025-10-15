import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import FilterPanel from './components/FilterPanel';
import ResultsList from './components/ResultsList';
import ExpertFinder from './components/ExpertFinder';
import StatsBar from './components/StatsBar';
import { sampleProjects, expertProfiles } from './data/sampleData';
import { API_ENDPOINTS, USE_SAMPLE_DATA } from './config';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
`;

const MainContent = styled.main`
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
`;

const ContentGrid = styled.div`
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 2rem;
  margin-top: 2rem;
  
  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
`;

const MainArea = styled.div`
  min-height: 400px;
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
`;

const EmptyStateIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.3;
`;

const EmptyStateTitle = styled.h2`
  font-size: 1.5rem;
  color: #475569;
  margin-bottom: 0.5rem;
  font-weight: 600;
`;

const EmptyStateText = styled.p`
  font-size: 1rem;
  color: #64748B;
  line-height: 1.6;
`;

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [recentSearches, setRecentSearches] = useState([]);
  const [filters, setFilters] = useState({
    minTrustScore: 0,
    categories: [],
    regions: [],
    experts: []
  });
  const [hasSearched, setHasSearched] = useState(false);
  const [selectedExpert, setSelectedExpert] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [totalProjects, setTotalProjects] = useState(6); // Default to 6, will update from API

  // Fetch total project count on mount
  useEffect(() => {
    const fetchStats = async () => {
      if (USE_SAMPLE_DATA) {
        setTotalProjects(sampleProjects.length);
        return;
      }
      
      try {
        const response = await axios.get(API_ENDPOINTS.stats);
        setTotalProjects(response.data.total_projects || 0);
      } catch (err) {
        console.error('Failed to fetch stats:', err);
        setTotalProjects(0);
      }
    };
    
    fetchStats();
  }, []);

  // Real API search function
  const performSearch = async (query) => {
    if (!query.trim()) {
      setSearchResults([]);
      setHasSearched(false);
      return;
    }

    setHasSearched(true);
    setIsLoading(true);
    setError(null);

    // Add to recent searches
    if (!recentSearches.includes(query)) {
      setRecentSearches([query, ...recentSearches.slice(0, 4)]);
    }

    // Use sample data if configured (for demo mode)
    if (USE_SAMPLE_DATA) {
      const lowerQuery = query.toLowerCase();
      let results = sampleProjects.filter(project => {
        const searchableText = `
          ${project.projectName} 
          ${project.description} 
          ${project.category}
          ${project.region}
          ${project.projectLeader}
          ${project.tags.join(' ')}
        `.toLowerCase();
        return searchableText.includes(lowerQuery);
      });

      // Apply filters
      results = results.filter(project => {
        if (project.trustScore < filters.minTrustScore) return false;
        if (filters.categories.length > 0 && !filters.categories.includes(project.category)) return false;
        if (filters.regions.length > 0 && !filters.regions.includes(project.region)) return false;
        return true;
      });

      results.sort((a, b) => b.similarityScore - a.similarityScore);
      setSearchResults(results);
      setIsLoading(false);
      return;
    }

    // Call real backend API
    try {
      const response = await axios.post(API_ENDPOINTS.search, {
        query: query,
        top_k: 10,
        min_trust_score: filters.minTrustScore / 100, // Convert to 0-1 scale
        categories: filters.categories,
        regions: filters.regions
      });

      setSearchResults(response.data.results);
      setIsLoading(false);
    } catch (err) {
      console.error('Search failed:', err);
      setError(err.response?.data?.detail || 'Search failed. Please try again.');
      setSearchResults([]);
      setIsLoading(false);
    }
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
    performSearch(query);
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    if (hasSearched) {
      performSearch(searchQuery);
    }
  };

  const handleExpertSelect = (expertName) => {
    const expert = expertProfiles.find(e => e.name === expertName);
    setSelectedExpert(expert);
  };

  const handleExpertClose = () => {
    setSelectedExpert(null);
  };

  const handleFeedback = async (projectId, isPositive) => {
    if (USE_SAMPLE_DATA) {
      console.log(`Feedback for project ${projectId}: ${isPositive ? 'positive' : 'negative'}`);
      return;
    }

    try {
      await axios.post(API_ENDPOINTS.feedback, {
        project_id: projectId,
        is_positive: isPositive,
        timestamp: new Date().toISOString()
      });
      console.log('Feedback submitted successfully');
    } catch (err) {
      console.error('Failed to submit feedback:', err);
    }
  };

  const handleLessonSubmit = async (projectId, lesson) => {
    if (USE_SAMPLE_DATA) {
      console.log(`New lesson for project ${projectId}:`, lesson);
      return;
    }

    try {
      await axios.post(API_ENDPOINTS.lessons, {
        project_id: projectId,
        text: lesson.text,
        phase: lesson.phase || 'General',
        author: lesson.author || 'Anonymous',
        date: new Date().toISOString()
      });
      console.log('Lesson submitted successfully');
    } catch (err) {
      console.error('Failed to submit lesson:', err);
    }
  };

  return (
    <AppContainer>
      <Header />
      
      <MainContent>
        <SearchBar 
          onSearch={handleSearch}
          recentSearches={recentSearches}
          totalProjects={totalProjects}
        />
        
        {hasSearched && (
          <StatsBar 
            resultCount={searchResults.length}
            totalProjects={totalProjects}
            searchQuery={searchQuery}
          />
        )}
        
        <ContentGrid>
          <FilterPanel 
            filters={filters}
            onFilterChange={handleFilterChange}
            experts={expertProfiles}
            onExpertSelect={handleExpertSelect}
          />
          
          <MainArea>
            {!hasSearched ? (
              <EmptyState>
                <EmptyStateIcon>🔍</EmptyStateIcon>
                <EmptyStateTitle>Search the Tonkin Knowledge Base</EmptyStateTitle>
                <EmptyStateText>
                  Enter a query to find relevant projects, documents, and expertise.<br/>
                  Try searching for "stormwater", "bridge design", or an engineer's name.
                </EmptyStateText>
              </EmptyState>
            ) : searchResults.length > 0 ? (
              <ResultsList 
                results={searchResults}
                onFeedback={handleFeedback}
                onLessonSubmit={handleLessonSubmit}
                onExpertClick={handleExpertSelect}
              />
            ) : (
              <EmptyState>
                <EmptyStateIcon>😔</EmptyStateIcon>
                <EmptyStateTitle>No results found</EmptyStateTitle>
                <EmptyStateText>
                  Try adjusting your search query or filters.<br/>
                  Make sure the spelling is correct or try different keywords.
                </EmptyStateText>
              </EmptyState>
            )}
          </MainArea>
        </ContentGrid>
      </MainContent>
      
      {selectedExpert && (
        <ExpertFinder 
          expert={selectedExpert}
          onClose={handleExpertClose}
          projects={sampleProjects.filter(p => 
            p.projectLeader === selectedExpert.name || 
            p.projectReviewer === selectedExpert.name
          )}
        />
      )}
    </AppContainer>
  );
}

export default App;

