from fastapi import APIRouter, Depends, UploadFile, File, Query
from modules.upload.uploadService import UploadService
from modules.permissions.permissionService import PermissionService

router = APIRouter()
upload_service = UploadService()
permission_service = PermissionService()

@router.post("/", tags=["Upload"])
async def upload_file(
    file: UploadFile = File(...),
    max_size: int = Query(None, description="Maximum file size in KB"),
    current_user: dict = Depends(permission_service.require_permission("upload", "create"))
):
    """Upload file to Cloudinary"""
    max_size_bytes = max_size * 1024 if max_size else None
    return await upload_service.upload_file(file, max_size_bytes)

@router.delete("/{public_id:path}", tags=["Upload"])
async def delete_file(
    public_id: str,
    current_user: dict = Depends(permission_service.require_permission("upload", "delete"))
):
    """Delete file from Cloudinary"""
    return await upload_service.delete_file(public_id)

@router.get("/download/{public_id:path}", tags=["Upload"])
async def download_file(
    public_id: str,
    current_user: dict = Depends(permission_service.require_permission("upload", "read"))
):
    """Get download URL for file"""
    from core.response import create_response
    import cloudinary
    
    try:
        url = cloudinary.CloudinaryImage(public_id).build_url()
        return create_response(
            message="Download URL generated successfully",
            data={"url": url, "public_id": public_id}
        )
    except Exception as e:
        return create_response(success=False, code=500, message=str(e), data=None)
