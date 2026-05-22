"""
API Routes - Authentication
Gestion de l'authentification OAuth Google Ads
"""

from fastapi import APIRouter, HTTPException, status, Depends, Header
from typing import Optional

from app.models.auth import (
    OAuthStartRequest,
    OAuthStartResponse,
    OAuthCallbackRequest,
    TokenResponse,
    AuthStatusResponse,
    LoginRequest
)
from app.services.google_ads_service import google_ads_service
from app.core.security import create_access_token, verify_token


router = APIRouter()


def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """
    Extrait le user_id du JWT token

    Returns:
        user_id ou None si non authentifié
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization.split(" ")[1]
    payload = verify_token(token)

    if payload:
        return payload.get("sub")

    return None


@router.post("/oauth/start", response_model=OAuthStartResponse)
async def start_oauth(request: OAuthStartRequest):
    """
    Démarre le flow OAuth Google Ads

    Returns:
        URL d'autorisation et state
    """
    try:
        if not google_ads_service.check_client_secret_exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="client_secret.json not found. Please configure Google Cloud OAuth credentials."
            )

        authorization_url, state = google_ads_service.get_authorization_url(
            redirect_uri=request.redirect_uri
        )

        return OAuthStartResponse(
            authorization_url=authorization_url,
            state=state
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start OAuth flow: {str(e)}"
        )


@router.post("/oauth/callback", response_model=TokenResponse)
async def oauth_callback(request: OAuthCallbackRequest):
    """
    Callback OAuth - échange le code contre un token

    Returns:
        JWT access token
    """
    try:
        # Échange code contre refresh_token
        refresh_token = google_ads_service.exchange_code_for_token(
            code=request.code,
            redirect_uri="http://localhost:8080/callback"  # TODO: from session/state
        )

        # Créer un user_id temporaire (en production, utiliser un vrai système d'users)
        user_id = f"user_{request.state[:8]}"

        # Sauvegarder refresh_token (temporairement, en attente des autres credentials)
        # TODO: Stocker dans une session temporaire

        # Créer JWT token
        access_token = create_access_token(data={"sub": user_id})

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=60 * 24 * 60  # 24 hours in seconds
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth callback failed: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """
    Login avec credentials Google Ads complets

    Returns:
        JWT access token
    """
    try:
        # Valider les credentials
        is_valid = google_ads_service.validate_credentials(
            developer_token=credentials.developer_token,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            refresh_token=credentials.refresh_token
        )

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google Ads credentials"
            )

        # Formater et valider customer_id
        customer_id = google_ads_service.format_customer_id(credentials.customer_id)

        if not google_ads_service.validate_customer_id_format(customer_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid customer_id format (must be 10 digits)"
            )

        # Créer user_id basé sur customer_id
        user_id = f"gads_{customer_id}"

        # Sauvegarder credentials
        credentials_dict = {
            "developer_token": credentials.developer_token,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "refresh_token": credentials.refresh_token,
            "customer_id": customer_id,
            "login_customer_id": credentials.login_customer_id
        }

        google_ads_service.save_credentials(user_id, credentials_dict)

        # Créer JWT token
        access_token = create_access_token(data={"sub": user_id})

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=60 * 24 * 60  # 24 hours
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/status", response_model=AuthStatusResponse)
async def auth_status(user_id: Optional[str] = Depends(get_current_user)):
    """
    Vérifie l'état d'authentification

    Returns:
        État d'authentification et infos compte
    """
    if not user_id:
        return AuthStatusResponse(authenticated=False)

    # Charger credentials
    credentials = google_ads_service.load_credentials(user_id)

    if not credentials:
        return AuthStatusResponse(authenticated=False)

    # Récupérer infos du compte
    customer_id = credentials.get("customer_id")

    if customer_id:
        customer_info = google_ads_service.get_customer_info(
            developer_token=credentials["developer_token"],
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            refresh_token=credentials["refresh_token"],
            customer_id=customer_id
        )

        if customer_info:
            return AuthStatusResponse(
                authenticated=True,
                customer_id=customer_info["id"],
                customer_name=customer_info["name"],
                customer_currency=customer_info["currency"]
            )

    return AuthStatusResponse(
        authenticated=True,
        customer_id=customer_id
    )


@router.post("/logout")
async def logout(user_id: Optional[str] = Depends(get_current_user)):
    """
    Déconnecte l'utilisateur (supprime credentials)

    Returns:
        Confirmation
    """
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Supprimer credentials
    google_ads_service.delete_credentials(user_id)

    return {"message": "Logged out successfully", "user_id": user_id}

