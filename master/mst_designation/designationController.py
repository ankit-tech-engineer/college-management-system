from base.BaseController import BaseController
from master.mst_designation.designationService import DesignationService
from master.mst_designation.designationModel import DesignationCreateSchema, DesignationUpdateSchema

service = DesignationService()
base_controller = BaseController(service, DesignationCreateSchema, DesignationUpdateSchema, "designations")
router = base_controller.create_routes()
