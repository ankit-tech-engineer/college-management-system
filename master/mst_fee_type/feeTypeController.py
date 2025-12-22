from base.BaseController import BaseController
from master.mst_fee_type.feeTypeService import FeeTypeService
from master.mst_fee_type.feeTypeModel import FeeTypeCreateSchema, FeeTypeUpdateSchema

service = FeeTypeService()
base_controller = BaseController(service, FeeTypeCreateSchema, FeeTypeUpdateSchema, "fee_types")
router = base_controller.create_routes()
