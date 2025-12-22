from base.BaseController import BaseController
from master.mst_college.collegeService import CollegeService
from master.mst_college.collegeModel import CollegeCreateSchema, CollegeUpdateSchema

service = CollegeService()
base_controller = BaseController(service, CollegeCreateSchema, CollegeUpdateSchema, "colleges")
router = base_controller.create_routes()
