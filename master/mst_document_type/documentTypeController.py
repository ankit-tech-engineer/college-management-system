from base.BaseController import BaseController
from master.mst_document_type.documentTypeService import DocumentTypeService
from master.mst_document_type.documentTypeModel import DocumentTypeCreateSchema, DocumentTypeUpdateSchema

service = DocumentTypeService()
base_controller = BaseController(service, DocumentTypeCreateSchema, DocumentTypeUpdateSchema, "document_types")
router = base_controller.create_routes()
