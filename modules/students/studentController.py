from fastapi import APIRouter, Depends, Response
from modules.students.studentModel import UpdateApplicationStatusModel
from modules.students.studentService import StudentService
from modules.permissions.permissionService import PermissionService

router = APIRouter()
student_service = StudentService()
permission_service = PermissionService()

@router.patch("/{student_id}/application-status")
async def update_application_status(
    student_id: str,
    status_data: UpdateApplicationStatusModel,
    response: Response,
    current_user: dict = Depends(permission_service.require_permission("students", "update"))
):
    """
    Update student application status (admin only)
    """
    result = await student_service.update_application_status(student_id, status_data.application_status)
    response.status_code = result.get("code", 200)
    return result
