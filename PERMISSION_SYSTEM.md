# Role-Based Permission System

## Overview
Complete role-based access control (RBAC) system with resource-based permissions and action-level authorization.

## Architecture

### 1. Permission Service (`modules/permissions/permissionService.py`)
- **check_permission(user_role, resource, action)**: Validates if a role has permission for a specific resource and action
- **require_permission(resource, action)**: FastAPI dependency that enforces permission checks on routes
- **get_all_permissions()**: Returns all available resources and actions

### 2. Available Resources and Actions

```python
RESOURCES = {
    "users": ["read", "create", "update", "delete"],
    "roles": ["read", "create", "update", "delete"],
    "permissions": ["read"],
    "auth": ["read", "create"],
    "otp": ["read", "create"],
    "password": ["update"],
    "students": ["read", "create", "update", "delete"],
    "staff": ["read", "create", "update", "delete"],
    "courses": ["read", "create", "update", "delete"],
    "departments": ["read", "create", "update", "delete"],
    "classrooms": ["read", "create", "update", "delete"],
    "attendance": ["read", "create", "update", "delete"],
    "exams": ["read", "create", "update", "delete"],
    "fees": ["read", "create", "update", "delete"],
    "library": ["read", "create", "update", "delete"],
    "hostel": ["read", "create", "update", "delete"],
    "transport": ["read", "create", "update", "delete"],
    "canteen": ["read", "create", "update", "delete"],
    "events": ["read", "create", "update", "delete"],
    "timetable": ["read", "create", "update", "delete"],
    "notifications": ["read", "create", "update", "delete"],
    "reports": ["read", "create"]
}
```

## Usage in Controllers

### Basic Pattern
```python
from fastapi import APIRouter, Depends
from modules.permissions.permissionService import PermissionService

router = APIRouter()
permission_service = PermissionService()

@router.get("/")
async def get_items(current_user: dict = Depends(permission_service.require_permission("resource", "read"))):
    """Get all items"""
    return {"message": "Success"}

@router.post("/")
async def create_item(current_user: dict = Depends(permission_service.require_permission("resource", "create"))):
    """Create item"""
    return {"message": "Created"}

@router.put("/{id}")
async def update_item(id: str, current_user: dict = Depends(permission_service.require_permission("resource", "update"))):
    """Update item"""
    return {"message": "Updated"}

@router.delete("/{id}")
async def delete_item(id: str, current_user: dict = Depends(permission_service.require_permission("resource", "delete"))):
    """Delete item"""
    return {"message": "Deleted"}
```

## Default Roles

### Admin Role
- Full access to all resources and actions
- Can manage users, roles, permissions
- Can perform all CRUD operations on all modules

### Student Role
- Read-only access to: courses, attendance, exams, fees, library, timetable, events
- Can manage own auth and password

### Teacher Role
- Read access to students
- Read/Update access to courses
- Read/Create/Update access to attendance and exams
- Read/Create access to reports
- Can manage own auth and password

## Implementation Status

### ✅ Completed Controllers
- **authController.py**: Auth endpoints with permission checks on /me and /change-password
- **roleController.py**: All CRUD operations with permission checks (create, read, update, delete)
- **permissionController.py**: Read permissions with permission check
- **otpController.py**: Public endpoints (no permission checks needed)
- **userController.py**: Full CRUD with permission checks
- **studentController.py**: Full CRUD with permission checks

### 📝 Template Available
- See `CONTROLLER_TEMPLATE.md` for implementation pattern
- Apply to remaining controllers as needed

## Public Endpoints (No Permission Required)
- POST /auth/register
- POST /auth/login
- POST /auth/token
- POST /auth/forgot-password
- POST /auth/reset-password
- POST /otp/verify
- POST /otp/regenerate

## Protected Endpoints (Permission Required)
All other endpoints require:
1. Valid JWT token (authentication)
2. Appropriate role permission (authorization)

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "detail": "Permission denied: resource.action"
}
```

## Testing Permissions

1. Initialize roles: `python init_roles.py`
2. Register users with different roles
3. Login to get JWT token
4. Test endpoints with different role tokens
5. Verify permission checks work correctly

## Adding New Resources

1. Add resource to `RESOURCES` dict in `permissionService.py`
2. Update `init_roles.py` with appropriate permissions for each role
3. Apply permission checks in controller using `require_permission()`
4. Re-run `python init_roles.py` to update existing roles (if needed)

## Best Practices

1. Always use `permission_service.require_permission()` for protected routes
2. Keep public endpoints (register, login) without permission checks
3. Use descriptive resource names matching your module names
4. Use standard actions: read, create, update, delete
5. Test with different roles to ensure proper access control
