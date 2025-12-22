from datetime import datetime
from config.database import get_db
from core.response import create_response
from bson import ObjectId

class StudentService:
    async def get_collection(self):
        db = await get_db()
        return db["students"]
    
    async def update_application_status(self, student_id: str, status: str):
        try:
            db = await get_db()
            students_collection = db["students"]
            users_collection = db["users"]
            
            student = await students_collection.find_one({"id": int(student_id), "is_deleted": False})
            
            if not student:
                return create_response(
                    success=False,
                    code=404,
                    message="Student not found",
                    data=None
                )
            
            await students_collection.update_one(
                {"id": int(student_id)},
                {"$set": {
                    "application_status": status,
                    "updated_at": datetime.utcnow()
                }}
            )
            
            await users_collection.update_one(
                {"id": student["user_id"]},
                {"$set": {
                    "application_status": status,
                    "updated_at": datetime.utcnow()
                }}
            )
            
            return create_response(
                message="Application status updated successfully",
                data={"application_status": status}
            )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
