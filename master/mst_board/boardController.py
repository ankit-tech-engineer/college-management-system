from base.BaseController import BaseController
from master.mst_board.boardService import BoardService
from master.mst_board.boardModel import BoardCreateSchema, BoardUpdateSchema

service = BoardService()
base_controller = BaseController(service, BoardCreateSchema, BoardUpdateSchema, "boards")
router = base_controller.create_routes()
