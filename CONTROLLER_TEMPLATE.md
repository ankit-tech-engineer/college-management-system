# Controller Template with Role-Based Permissions

## Pattern for All Controllers

```python
from fastapi import APIRouter, Depends
from modules.permissions.permissionService import PermissionService

router = APIRouter()
permission_service = PermissionService()

# READ - Get all items
@router.get("/", tags=["ResourceName"])
async def get_all_items(current_user: dict = Depends(permission_service.require_permission("resource", "read"))):
    """Get all items"""
    return {"message": "Get all items"}

# CREATE - Create new item
@router.post("/", tags=["ResourceName"])
async def create_item(current_user: dict = Depends(permission_service.require_permission("resource", "create"))):
    """Create a new item"""
    return {"message": "Create item"}

# READ - Get single item
@router.get("/{item_id}", tags=["ResourceName"])
async def get_item(item_id: str, current_user: dict = Depends(permission_service.require_permission("resource", "read"))):
    """Get item by ID"""
    return {"message": f"Get item {item_id}"}

# UPDATE - Update item
@router.put("/{item_id}", tags=["ResourceName"])
async def update_item(item_id: str, current_user: dict = Depends(permission_service.require_permission("resource", "update"))):
    """Update item"""
    return {"message": f"Update item {item_id}"}

# DELETE - Delete item
@router.delete("/{item_id}", tags=["ResourceName"])
async def delete_item(item_id: str, current_user: dict = Depends(permission_service.require_permission("resource", "delete"))):
    """Delete item"""
    return {"message": f"Delete item {item_id}"}
```

## Available Resources and Actions

### Resources:
- users: read, create, update, delete
- roles: read, create, update, delete
- permissions: read
- auth: read, create
- otp: read, create
- password: update
- students: read, create, update, delete
- staff: read, create, update, delete
- courses: read, create, update, delete
- departments: read, create, update, delete
- classrooms: read, create, update, delete
- attendance: read, create, update, delete
- exams: read, create, update, delete
- fees: read, create, update, delete
- library: read, create, update, delete
- hostel: read, create, update, delete
- transport: read, create, update, delete
- canteen: read, create, update, delete
- events: read, create, update, delete
- timetable: read, create, update, delete
- notifications: read, create, update, delete
- reports: read, create

## Usage Instructions

1. Import PermissionService in your controller
2. Create permission_service instance
3. Use `Depends(permission_service.require_permission("resource", "action"))` in route parameters
4. Replace "resource" with the actual resource name (e.g., "students", "courses")
5. Replace "action" with the actual action (e.g., "read", "create", "update", "delete")

## Public Endpoints (No Permission Check)

For public endpoints like register, login, verify-otp, forgot-password:
- Do NOT add permission checks
- These endpoints should be accessible without authentication

## Example Implementations

See:
- modules/user/userController.py
- modules/student/studentController.py
- modules/roles/roleController.py
- modules/auth/authController.py
