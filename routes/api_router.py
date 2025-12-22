from fastapi import APIRouter
from core.sys_req_log.req_log_controller import router as req_log_router
from modules.auth.authController import router as auth_router
from modules.otp.otpController import router as otp_router
from modules.upload.uploadController import router as upload_router
from modules.roles.roleController import router as role_router
from modules.permissions.permissionController import router as permission_router
from modules.resources.resourceController import router as resource_router
from modules.common.country.countryController import router as country_router
from modules.common.state.stateController import router as state_router
from modules.common.city.cityController import router as city_router
from modules.students.studentController import router as student_router
from master.mst_college.collegeController import router as college_router
from master.mst_board.boardController import router as board_router
from master.mst_department.departmentController import router as department_router
from master.mst_course.courseController import router as course_router
from master.mst_branch.branchController import router as branch_router
from master.mst_program.programController import router as program_router
from master.mst_semester.semesterController import router as semester_router
from master.mst_admission_category.admissionCategoryController import router as admission_category_router
from master.mst_document_type.documentTypeController import router as document_type_router
from master.mst_designation.designationController import router as designation_router
from master.mst_fee_type.feeTypeController import router as fee_type_router

api_router = APIRouter()

api_router.include_router(req_log_router, prefix="/system", tags=["System"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(otp_router, prefix="/otp", tags=["OTP Verification"])
api_router.include_router(upload_router, prefix="/upload", tags=["Upload"])
api_router.include_router(role_router, prefix="/roles", tags=["Roles"])
api_router.include_router(permission_router, prefix="/permissions", tags=["Permissions"])
api_router.include_router(resource_router, prefix="/resources", tags=["Resources"])
api_router.include_router(country_router, prefix="/countries", tags=["Countries"])
api_router.include_router(state_router, prefix="/states", tags=["States"])
api_router.include_router(city_router, prefix="/cities", tags=["Cities"])
api_router.include_router(student_router, prefix="/students", tags=["Students"])
api_router.include_router(college_router, prefix="/colleges", tags=["Colleges"])
api_router.include_router(board_router, prefix="/boards", tags=["Boards"])
api_router.include_router(department_router, prefix="/departments", tags=["Departments"])
api_router.include_router(course_router, prefix="/courses", tags=["Courses"])
api_router.include_router(branch_router, prefix="/branches", tags=["Branches"])
api_router.include_router(program_router, prefix="/programs", tags=["Programs"])
api_router.include_router(semester_router, prefix="/semesters", tags=["Semesters"])
api_router.include_router(admission_category_router, prefix="/admission-categories", tags=["Admission Categories"])
api_router.include_router(document_type_router, prefix="/document-types", tags=["Document Types"])
api_router.include_router(designation_router, prefix="/designations", tags=["Designations"])
api_router.include_router(fee_type_router, prefix="/fee-types", tags=["Fee Types"])