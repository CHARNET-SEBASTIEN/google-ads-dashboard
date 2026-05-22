"""
Pydantic Models - Authentication
"""

from typing import Optional
from pydantic import BaseModel, Field


class OAuthStartRequest(BaseModel):
    """Request to start OAuth flow"""
    redirect_uri: Optional[str] = "http://localhost:8080/callback"


class OAuthStartResponse(BaseModel):
    """Response with OAuth URL"""
    authorization_url: str
    state: str


class OAuthCallbackRequest(BaseModel):
    """OAuth callback with auth code"""
    code: str
    state: str


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthStatusResponse(BaseModel):
    """Authentication status"""
    authenticated: bool
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    customer_currency: Optional[str] = None


class GoogleAdsCredentials(BaseModel):
    """Google Ads credentials"""
    developer_token: str
    client_id: str
    client_secret: str
    refresh_token: str
    customer_id: str
    login_customer_id: Optional[str] = None


class LoginRequest(BaseModel):
    """Manual login with credentials"""
    developer_token: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    client_secret: str = Field(..., min_length=1)
    refresh_token: str = Field(..., min_length=1)
    customer_id: str = Field(..., pattern=r'^\d{10}$')
    login_customer_id: Optional[str] = Field(None, pattern=r'^\d{10}$')
