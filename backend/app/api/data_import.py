"""
API Routes - Data Import
Import de données JSON et Google Drive
"""

import json
import tempfile
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from pydantic import BaseModel

from app.services.data_loader_service import data_loader_service


router = APIRouter()


class GoogleDriveImportRequest(BaseModel):
    """Request pour import Google Drive"""
    file_id: str


class DataStatusResponse(BaseModel):
    """Response pour le statut des données"""
    data_exists: bool
    last_update: Optional[str] = None
    account_info: Optional[dict] = None
    stats: dict
    drive_config: Optional[dict] = None


class ImportResponse(BaseModel):
    """Response après import"""
    success: bool
    message: str
    stats: dict


@router.post("/import-json", response_model=ImportResponse)
async def import_json(file: UploadFile = File(...)):
    """
    Upload et importe un fichier JSON

    Args:
        file: Fichier JSON uploadé

    Returns:
        Résultat de l'import avec statistiques
    """
    try:
        # Vérifier le type de fichier
        if not file.filename.endswith('.json'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a JSON file"
            )

        # Lire le contenu
        content = await file.read()

        # Valider JSON
        try:
            data = json.loads(content.decode('utf-8'))
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON format"
            )

        # Valider les champs requis
        required_fields = ['campaigns', 'keywords', 'ads']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )

        # Sauvegarder dans un fichier temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            json.dump(data, tmp_file)
            tmp_file_path = tmp_file.name

        # Importer via le service
        success = data_loader_service.import_from_file(tmp_file_path)

        # Nettoyer le fichier temporaire
        Path(tmp_file_path).unlink(missing_ok=True)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to import data"
            )

        # Récupérer les stats
        stats = data_loader_service.get_stats()

        return ImportResponse(
            success=True,
            message=f"Data imported successfully: {stats['campaigns']} campaigns, "
                    f"{stats['keywords']} keywords, {stats['ads']} ads",
            stats=stats
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Import failed: {str(e)}"
        )


@router.post("/import-google-drive", response_model=ImportResponse)
async def import_google_drive(request: GoogleDriveImportRequest):
    """
    Télécharge et importe les données depuis Google Drive

    Args:
        request: Contient file_id du fichier Google Drive

    Returns:
        Résultat de l'import avec statistiques
    """
    try:
        if not request.file_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="file_id is required"
            )

        # Télécharger depuis Google Drive
        success = data_loader_service.download_from_google_drive(request.file_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to download from Google Drive. "
                       "Check file_id and ensure file is publicly accessible."
            )

        # Récupérer les stats
        stats = data_loader_service.get_stats()

        return ImportResponse(
            success=True,
            message=f"Data downloaded from Google Drive: {stats['campaigns']} campaigns, "
                    f"{stats['keywords']} keywords, {stats['ads']} ads",
            stats=stats
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Google Drive import failed: {str(e)}"
        )


@router.get("/status", response_model=DataStatusResponse)
async def data_status():
    """
    Retourne l'état des données actuelles

    Returns:
        Statut des données avec infos compte et statistiques
    """
    data_exists = data_loader_service.data_exists()
    drive_config = data_loader_service.get_drive_config()

    if not data_exists:
        return DataStatusResponse(
            data_exists=False,
            last_update=None,
            account_info=None,
            stats={"campaigns": 0, "keywords": 0, "ads": 0, "search_terms": 0},
            drive_config=drive_config
        )

    last_update = data_loader_service.get_last_update()
    account_info = data_loader_service.get_account_info()
    stats = data_loader_service.get_stats()

    return DataStatusResponse(
        data_exists=True,
        last_update=last_update,
        account_info=account_info,
        stats=stats,
        drive_config=drive_config
    )


@router.post("/refresh-from-drive", response_model=ImportResponse)
async def refresh_from_drive():
    """
    Rafraîchit les données depuis le dernier fichier Google Drive configuré

    Returns:
        Résultat de l'import avec statistiques
    """
    try:
        # Vérifier qu'une config Drive existe
        config = data_loader_service.get_drive_config()
        if not config or 'file_id' not in config:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Google Drive file configured. Please import from Drive first."
            )

        # Rafraîchir les données
        success = data_loader_service.refresh_from_drive()

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to refresh from Google Drive. Check file accessibility."
            )

        # Récupérer les stats
        stats = data_loader_service.get_stats()

        return ImportResponse(
            success=True,
            message=f"Data refreshed from Google Drive: {stats['campaigns']} campaigns, "
                    f"{stats['keywords']} keywords, {stats['ads']} ads",
            stats=stats
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Refresh failed: {str(e)}"
        )


@router.delete("/clear")
async def clear_data():
    """
    Supprime toutes les données locales

    Returns:
        Confirmation
    """
    try:
        if data_loader_service.data_file.exists():
            data_loader_service.data_file.unlink()

        return {"success": True, "message": "Data cleared successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear data: {str(e)}"
        )

