from base.BaseController import BaseController
from master.mst_semester.semesterService import SemesterService
from master.mst_semester.semesterModel import SemesterCreateSchema, SemesterUpdateSchema

service = SemesterService()
base_controller = BaseController(service, SemesterCreateSchema, SemesterUpdateSchema, "semesters")
router = base_controller.create_routes()
