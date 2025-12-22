from base.BaseController import BaseController
from master.mst_course.courseService import CourseService
from master.mst_course.courseModel import CourseCreateSchema, CourseUpdateSchema

service = CourseService()
base_controller = BaseController(service, CourseCreateSchema, CourseUpdateSchema, "courses")
router = base_controller.create_routes()
