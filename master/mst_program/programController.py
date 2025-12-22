from base.BaseController import BaseController
from master.mst_program.programService import ProgramService
from master.mst_program.programModel import ProgramCreateSchema, ProgramUpdateSchema

service = ProgramService()
base_controller = BaseController(service, ProgramCreateSchema, ProgramUpdateSchema, "programs")
router = base_controller.create_routes()
