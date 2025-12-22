import cloudinary
import cloudinary.uploader
from config.settings import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, MAX_FILE_SIZE
from core.response import create_response
from fastapi import UploadFile

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

class UploadService:
    ALLOWED_EXTENSIONS = {
        'image': ['png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'],
        'video': ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'],
        'audio': ['mp3', 'wav', 'ogg', 'aac', 'm4a'],
        'document': ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'csv']
    }
    
    def get_resource_type(self, filename: str) -> str:
        ext = filename.split('.')[-1].lower()
        if ext in self.ALLOWED_EXTENSIONS['image']:
            return 'image'
        elif ext in self.ALLOWED_EXTENSIONS['video']:
            return 'video'
        elif ext in self.ALLOWED_EXTENSIONS['audio']:
            return 'video'  # Cloudinary uses 'video' for audio
        else:
            return 'raw'
    
    async def upload_file(self, file: UploadFile, max_size: int = 2048):
        try:
            if max_size is None:
                max_size = MAX_FILE_SIZE
            
            contents = await file.read()
            file_size = len(contents)
            
            if file_size > max_size:
                return create_response(
                    success=False,
                    code=400,
                    message=f"File size exceeds maximum allowed size of {max_size / 1024}KB",
                    data=None
                )
            
            resource_type = self.get_resource_type(file.filename)
            
            result = cloudinary.uploader.upload(
                contents,
                resource_type=resource_type,
                folder="college_management"
            )
            
            return create_response(
                message="File uploaded successfully",
                data={
                    "url": result.get("secure_url"),
                    "public_id": result.get("public_id"),
                    "format": result.get("format"),
                    "resource_type": result.get("resource_type"),
                    "size": result.get("bytes"),
                    "filename": file.filename
                }
            )
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def delete_file(self, public_id: str):
        try:
            result = cloudinary.uploader.destroy(public_id)
            
            if result.get("result") == "ok":
                return create_response(message="File deleted successfully", data=None)
            else:
                return create_response(success=False, code=404, message="File not found", data=None)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
