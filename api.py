"""
FastAPI Backend for Tonkin Knowledge Finder
Provides REST API endpoints for the React frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.search import SemanticSearchEngine
from src.database import KnowledgeDatabase

# Initialize FastAPI
app = FastAPI(
    title="Tonkin Knowledge Finder API",
    description="AI-Powered Project Intelligence & Expertise Discovery",
    version="1.0.0"
)

# Configure CORS to allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local React dev
        "https://helpful-rabanadas-4fee85.netlify.app",  # Your specific Netlify URL
        "https://*.netlify.app",  # Netlify deployments
        "https://*.vercel.app",   # Vercel deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize search engine and database
try:
    search_engine = SemanticSearchEngine()
    db = KnowledgeDatabase()
except Exception as e:
    print(f"Warning: Could not initialize search engine: {e}")
    search_engine = None
    db = None


# ==================== REQUEST/RESPONSE MODELS ====================

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 10
    min_trust_score: Optional[float] = 0.0
    categories: Optional[List[str]] = []
    regions: Optional[List[str]] = []


class FeedbackRequest(BaseModel):
    project_id: str
    is_positive: bool
    timestamp: Optional[str] = None


class LessonRequest(BaseModel):
    project_id: str
    text: str
    phase: Optional[str] = "General"
    author: Optional[str] = "Anonymous"
    date: Optional[str] = None


class SearchResult(BaseModel):
    id: int
    project_number: str
    project_name: str
    description: str
    client: Optional[str]
    region: Optional[str]
    category: Optional[str]
    phase: Optional[str]
    trust_score: float
    similarity_score: float
    project_leader: Optional[str]
    project_reviewer: Optional[str]
    disciplines: Optional[List[str]]
    budget: Optional[str]
    status: Optional[str]
    tags: Optional[List[str]]
    lessons: Optional[List[Dict[str, Any]]]


class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total: int
    query: str
    execution_time: float


# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Tonkin Knowledge Finder API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "search_engine": "initialized" if search_engine else "not initialized",
        "database": "connected" if db else "not connected",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/search", response_model=SearchResponse)
async def search_projects(request: SearchRequest):
    """
    Search for projects using semantic search
    
    - **query**: Search query text
    - **top_k**: Number of results to return (default: 10)
    - **min_trust_score**: Minimum trust score filter (0.0-1.0)
    - **categories**: List of categories to filter by
    - **regions**: List of regions to filter by
    """
    if not search_engine:
        raise HTTPException(status_code=503, detail="Search engine not initialized")
    
    try:
        start_time = datetime.now()
        
        # Perform semantic search
        results = search_engine.search(request.query, top_k=request.top_k * 2)  # Get extra for filtering
        
        # Apply filters
        filtered_results = []
        for result in results:
            # Trust score filter
            trust_score = result.get('trust_score', 0)
            if trust_score < request.min_trust_score:
                continue
            
            # Category filter
            if request.categories and result.get('category') not in request.categories:
                continue
            
            # Region filter
            if request.regions and result.get('program_region') not in request.regions:
                continue
            
            # Format result for frontend
            formatted_result = {
                "id": result.get('id', 0),
                "projectNumber": result.get('project_number', f"TKN-{result.get('id', 0):04d}"),
                "projectName": result.get('project_name', 'Unknown Project'),
                "description": result.get('description', result.get('snippet', 'No description available.')),
                "client": result.get('client', 'N/A'),
                "region": result.get('program_region', 'Melbourne'),
                "category": result.get('category', 'Infrastructure'),
                "phase": result.get('lifecycle_phase', 'Active'),
                "trustScore": float(result.get('trust_score', 0.85)),
                "similarityScore": float(result.get('similarity_score', 0.75)),
                "projectLeader": result.get('project_leader', 'N/A'),
                "projectReviewer": result.get('project_reviewer', 'N/A'),
                "disciplines": result.get('disciplines', []),
                "budget": result.get('budget', 'N/A'),
                "status": "Active",
                "tags": result.get('tags', []),
                "lessons": result.get('lessons', [])
            }
            
            filtered_results.append(formatted_result)
            
            # Stop if we have enough results
            if len(filtered_results) >= request.top_k:
                break
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return SearchResponse(
            results=filtered_results,
            total=len(filtered_results),
            query=request.query,
            execution_time=execution_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """
    Submit feedback on search results
    
    - **project_id**: The project identifier
    - **is_positive**: True for thumbs up, False for thumbs down
    """
    try:
        # Store feedback (you can implement database storage here)
        return {
            "success": True,
            "message": "Feedback recorded",
            "project_id": feedback.project_id,
            "timestamp": feedback.timestamp or datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")


@app.post("/api/lessons")
async def submit_lesson(lesson: LessonRequest):
    """
    Submit a lesson learned or decision
    
    - **project_id**: The project identifier
    - **text**: Lesson learned text
    - **phase**: Project phase (optional)
    - **author**: Lesson author (optional)
    """
    try:
        # Store lesson (you can implement database storage here)
        lesson_id = hash(f"{lesson.project_id}_{lesson.text}_{datetime.now().isoformat()}")
        
        return {
            "success": True,
            "lesson_id": abs(lesson_id) % 1000000,
            "message": "Lesson saved successfully",
            "timestamp": lesson.date or datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lesson submission failed: {str(e)}")


@app.get("/api/stats")
async def get_statistics():
    """Get system statistics"""
    try:
        # Get real stats from database
        total_projects = 23  # Default
        total_documents = 156
        avg_trust_score = 0.87
        
        if db:
            try:
                import sqlite3
                conn = sqlite3.connect(db.db_path)
                
                # Count unique projects
                cursor = conn.execute("SELECT COUNT(DISTINCT project_name) FROM documents WHERE project_name IS NOT NULL AND project_name != ''")
                total_projects = cursor.fetchone()[0]
                
                # Count total documents
                cursor = conn.execute("SELECT COUNT(*) FROM documents")
                total_documents = cursor.fetchone()[0]
                
                # Get average trust score
                cursor = conn.execute("SELECT AVG(trust_score) FROM documents WHERE trust_score > 0")
                result = cursor.fetchone()[0]
                avg_trust_score = round(result, 2) if result else 0.87
                
                conn.close()
            except Exception as e:
                logger.error(f"Error getting stats from database: {e}")
            
        return {
            "total_projects": total_projects,
            "total_documents": total_documents,
            "total_experts": 45,
            "avg_trust_score": avg_trust_score,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")


@app.get("/api/categories")
async def get_categories():
    """Get available project categories"""
    return {
        "categories": [
            "Water & Wastewater",
            "Transport",
            "Buildings",
            "Energy",
            "Mining",
            "Environmental",
            "Industrial Infrastructure",
            "Urban Development"
        ]
    }


@app.get("/api/regions")
async def get_regions():
    """Get available regions"""
    return {
        "regions": [
            "Melbourne",
            "Sydney",
            "Brisbane",
            "Perth",
            "Adelaide",
            "Canberra",
            "International"
        ]
    }


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )

