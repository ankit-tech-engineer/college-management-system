import asyncio
from config.database import connect_db, get_db
from datetime import datetime

async def init_default_resources():
    """Initialize default resources"""
    db = await get_db()
    resources_collection = db["resources"]
    
    default_resources = [
        {"id": 1, "key": "users", "name": "Users", "actions": ["read", "create", "update", "delete"]},
        {"id": 2, "key": "roles", "name": "Roles", "actions": ["read", "create", "update", "delete"]},
        {"id": 3, "key": "permissions", "name": "Permissions", "actions": ["read", "create", "update", "delete"]},
        {"id": 4, "key": "resources", "name": "Resources", "actions": ["read", "create", "update", "delete"]},
        {"id": 5, "key": "auth", "name": "Auth", "actions": ["read", "create"]},
        {"id": 6, "key": "otp", "name": "OTP", "actions": ["read", "create"]},
        {"id": 7, "key": "password", "name": "Password", "actions": ["update"]},
        {"id": 8, "key": "students", "name": "Students", "actions": ["read", "create", "update", "delete"]},
        {"id": 9, "key": "staff", "name": "Staff", "actions": ["read", "create", "update", "delete"]},
        {"id": 10, "key": "courses", "name": "Courses", "actions": ["read", "create", "update", "delete"]},
        {"id": 11, "key": "departments", "name": "Departments", "actions": ["read", "create", "update", "delete"]},
        {"id": 12, "key": "classrooms", "name": "Classrooms", "actions": ["read", "create", "update", "delete"]},
        {"id": 13, "key": "attendance", "name": "Attendance", "actions": ["read", "create", "update", "delete"]},
        {"id": 14, "key": "exams", "name": "Exams", "actions": ["read", "create", "update", "delete"]},
        {"id": 15, "key": "fees", "name": "Fees", "actions": ["read", "create", "update", "delete"]},
        {"id": 16, "key": "library", "name": "Library", "actions": ["read", "create", "update", "delete"]},
        {"id": 17, "key": "hostel", "name": "Hostel", "actions": ["read", "create", "update", "delete"]},
        {"id": 18, "key": "transport", "name": "Transport", "actions": ["read", "create", "update", "delete"]},
        {"id": 19, "key": "canteen", "name": "Canteen", "actions": ["read", "create", "update", "delete"]},
        {"id": 20, "key": "events", "name": "Events", "actions": ["read", "create", "update", "delete"]},
        {"id": 21, "key": "timetable", "name": "Timetable", "actions": ["read", "create", "update", "delete"]},
        {"id": 22, "key": "notifications", "name": "Notifications", "actions": ["read", "create", "update", "delete"]},
        {"id": 23, "key": "reports", "name": "Reports", "actions": ["read", "create"]},
        {"id": 24, "key": "upload", "name": "Upload", "actions": ["read", "create", "delete"]},
        {"id": 25, "key": "countries", "name": "Countries", "actions": ["read", "create", "update", "delete"]},
        {"id": 26, "key": "states", "name": "States", "actions": ["read", "create", "update", "delete"]},
        {"id": 27, "key": "cities", "name": "Cities", "actions": ["read", "create", "update", "delete"]},
        {"id": 28, "key": "colleges", "name": "Colleges", "actions": ["read", "create", "update", "delete"]},
        {"id": 29, "key": "boards", "name": "Boards", "actions": ["read", "create", "update", "delete"]},
        {"id": 30, "key": "branches", "name": "Branches", "actions": ["read", "create", "update", "delete"]},
        {"id": 31, "key": "programs", "name": "Programs", "actions": ["read", "create", "update", "delete"]},
        {"id": 32, "key": "semesters", "name": "Semesters", "actions": ["read", "create", "update", "delete"]},
        {"id": 33, "key": "admission_categories", "name": "Admission Categories", "actions": ["read", "create", "update", "delete"]},
        {"id": 34, "key": "document_types", "name": "Document Types", "actions": ["read", "create", "update", "delete"]},
        {"id": 35, "key": "designations", "name": "Designations", "actions": ["read", "create", "update", "delete"]},
        {"id": 36, "key": "fee_types", "name": "Fee Types", "actions": ["read", "create", "update", "delete"]}
    ]
    
    for resource in default_resources:
        existing = await resources_collection.find_one({"key": resource["key"]})
        if not existing:
            resource["is_deleted"] = False
            resource["created_at"] = datetime.utcnow()
            resource["updated_at"] = datetime.utcnow()
            await resources_collection.insert_one(resource)
            print(f"Created resource: {resource['name']}")
        else:
            print(f"Resource already exists: {resource['name']}")

async def init_default_roles():
    """Initialize default roles and permissions"""
    await connect_db()
    db = await get_db()
    roles_collection = db["roles"]
    
    await init_default_resources()
    
    # Super Admin - Full access to all resources
    super_admin_permissions = [
        {"resource": key, "actions": actions, "allowed_actions": actions}
        for _, key, _, actions in [
            (1, "users", "Users", ["read", "create", "update", "delete"]),
            (2, "roles", "Roles", ["read", "create", "update", "delete"]),
            (3, "permissions", "Permissions", ["read", "create", "update", "delete"]),
            (4, "resources", "Resources", ["read", "create", "update", "delete"]),
            (5, "auth", "Auth", ["read", "create"]),
            (6, "otp", "OTP", ["read", "create"]),
            (7, "password", "Password", ["update"]),
            (8, "students", "Students", ["read", "create", "update", "delete"]),
            (9, "staff", "Staff", ["read", "create", "update", "delete"]),
            (10, "courses", "Courses", ["read", "create", "update", "delete"]),
            (11, "departments", "Departments", ["read", "create", "update", "delete"]),
            (12, "classrooms", "Classrooms", ["read", "create", "update", "delete"]),
            (13, "attendance", "Attendance", ["read", "create", "update", "delete"]),
            (14, "exams", "Exams", ["read", "create", "update", "delete"]),
            (15, "fees", "Fees", ["read", "create", "update", "delete"]),
            (16, "library", "Library", ["read", "create", "update", "delete"]),
            (17, "hostel", "Hostel", ["read", "create", "update", "delete"]),
            (18, "transport", "Transport", ["read", "create", "update", "delete"]),
            (19, "canteen", "Canteen", ["read", "create", "update", "delete"]),
            (20, "events", "Events", ["read", "create", "update", "delete"]),
            (21, "timetable", "Timetable", ["read", "create", "update", "delete"]),
            (22, "notifications", "Notifications", ["read", "create", "update", "delete"]),
            (23, "reports", "Reports", ["read", "create"]),
            (24, "upload", "Upload", ["read", "create", "delete"]),
            (25, "countries", "Countries", ["read", "create", "update", "delete"]),
            (26, "states", "States", ["read", "create", "update", "delete"]),
            (27, "cities", "Cities", ["read", "create", "update", "delete"]),
            (28, "colleges", "Colleges", ["read", "create", "update", "delete"]),
            (29, "boards", "Boards", ["read", "create", "update", "delete"]),
            (30, "branches", "Branches", ["read", "create", "update", "delete"]),
            (31, "programs", "Programs", ["read", "create", "update", "delete"]),
            (32, "semesters", "Semesters", ["read", "create", "update", "delete"]),
            (33, "admission_categories", "Admission Categories", ["read", "create", "update", "delete"]),
            (34, "document_types", "Document Types", ["read", "create", "update", "delete"]),
            (35, "designations", "Designations", ["read", "create", "update", "delete"]),
            (36, "fee_types", "Fee Types", ["read", "create", "update", "delete"])
        ]
    ]
    
    default_roles = [
        {
            "id": 1,
            "role": "super-admin",
            "permissions": super_admin_permissions,
            "is_deleted": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": 2,
            "role": "admin",
            "permissions": super_admin_permissions[:24] + [
                {"resource": "countries", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "states", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "cities", "actions": ["read"], "allowed_actions": ["read"]},
            ] + super_admin_permissions[27:],
            "is_deleted": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": 3,
            "role": "student",
            "permissions": [
                {"resource": "auth", "actions": ["read", "create"], "allowed_actions": ["read", "create"]},
                {"resource": "otp", "actions": ["read", "create"], "allowed_actions": ["read", "create"]},
                {"resource": "password", "actions": ["update"], "allowed_actions": ["update"]},
                {"resource": "courses", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "attendance", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "exams", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "fees", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "library", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "timetable", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "events", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "upload", "actions": ["read", "create"], "allowed_actions": ["read", "create"]},
                {"resource": "countries", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "states", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "cities", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "colleges", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "boards", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "branches", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "programs", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "semesters", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "admission_categories", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "document_types", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "designations", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "fee_types", "actions": ["read"], "allowed_actions": ["read"]}
            ],
            "is_deleted": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": 4,
            "role": "teacher",
            "permissions": [
                {"resource": "auth", "actions": ["read", "create"], "allowed_actions": ["read", "create"]},
                {"resource": "otp", "actions": ["read", "create"], "allowed_actions": ["read", "create"]},
                {"resource": "password", "actions": ["update"], "allowed_actions": ["update"]},
                {"resource": "students", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "courses", "actions": ["read", "update"], "allowed_actions": ["read", "update"]},
                {"resource": "attendance", "actions": ["read", "create", "update"], "allowed_actions": ["read", "create", "update"]},
                {"resource": "exams", "actions": ["read", "create", "update"], "allowed_actions": ["read", "create", "update"]},
                {"resource": "timetable", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "reports", "actions": ["read", "create"], "allowed_actions": ["read", "create"]},
                {"resource": "upload", "actions": ["read", "create"], "allowed_actions": ["read", "create"]},
                {"resource": "countries", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "states", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "cities", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "colleges", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "boards", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "branches", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "programs", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "semesters", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "admission_categories", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "document_types", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "designations", "actions": ["read"], "allowed_actions": ["read"]},
                {"resource": "fee_types", "actions": ["read"], "allowed_actions": ["read"]}
            ],
            "is_deleted": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    for role in default_roles:
        existing = await roles_collection.find_one({"role": role["role"]})
        if not existing:
            await roles_collection.insert_one(role)
            print(f"Created role: {role['role']}")
        else:
            print(f"Role already exists: {role['role']}")

if __name__ == "__main__":
    asyncio.run(init_default_roles())
    print("\nInitialization completed!")
    print("Default resources and roles have been created.")
    print("Run the application and use the API to manage resources and roles.")
