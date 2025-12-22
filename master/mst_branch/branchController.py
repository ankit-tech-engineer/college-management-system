from base.BaseController import BaseController
from master.mst_branch.branchService import BranchService
from master.mst_branch.branchModel import BranchCreateSchema, BranchUpdateSchema

service = BranchService()
base_controller = BaseController(service, BranchCreateSchema, BranchUpdateSchema, "branches")
router = base_controller.create_routes()
