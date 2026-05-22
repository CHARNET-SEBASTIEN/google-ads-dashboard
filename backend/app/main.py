"""
FastAPI Application - Google Ads Dashboard
Point d'entrée principal de l'API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config.settings import settings
from app.api import auth, campaigns, search_terms, diagnostics, data_import


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    print("🚀 Starting Google Ads Dashboard API...")
    yield
    print("👋 Shutting down Google Ads Dashboard API...")


app = FastAPI(
    title="Google Ads Dashboard API",
    description="API backend pour le dashboard Google Ads",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(data_import.router, prefix="/api/data", tags=["Data Import"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["Campaigns"])
app.include_router(search_terms.router, prefix="/api/search-terms", tags=["Search Terms"])
app.include_router(diagnostics.router, prefix="/api/diagnostics", tags=["Diagnostics"])


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "message": "Google Ads Dashboard API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
