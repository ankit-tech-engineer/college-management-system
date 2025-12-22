from base.BaseController import BaseController
from master.mst_department.departmentService import DepartmentService
from master.mst_department.departmentModel import DepartmentCreateSchema, DepartmentUpdateSchema

service = DepartmentService()
base_controller = BaseController(service, DepartmentCreateSchema, DepartmentUpdateSchema, "departments")
router = base_controller.create_routes()
