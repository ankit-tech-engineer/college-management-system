# Resource Management System

## Overview

Complete CRUD system for managing resources (permissions) dynamically. Resources define what actions can be performed on different parts of the system.

## Resource Structure

```json
{
  "id": 1,
  "key": "roles",
  "name": "Roles",
  "actions": ["read", "create", "update", "delete"],
  "is_deleted": false,
  "created_at": "2025-10-04T09:36:34.130Z",
  "updated_at": "2025-10-04T09:36:34.130Z"
}
```

### Fields

- **id**: Auto-incremented unique identifier
- **key**: Auto-generated from name (lowercase, spaces replaced with underscores)
- **name**: Display name of the resource
- **actions**: Array of available actions for this resource
- **is_deleted**: Soft delete flag
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

## Key Generation

Keys are automatically generated from the name:

- Spaces replaced with underscores
- Converted to lowercase
- Trimmed of whitespace

**Examples:**

- "User Management" → "user_management"
- "Roles" → "roles"
- "Student Records" → "student_records"

## API Endpoints

### Create Resource

```http
POST /permissions/resources
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "Roles",
    "actions": ["read", "create", "update", "delete"]
}
```

**Response:**

```json
{
  "success": true,
  "code": 200,
  "meta": {},
  "message": "Resource created successfully",
  "data": {
    "resource_id": "507f1f77bcf86cd799439011",
    "key": "roles"
  }
}
```

### Get All Resources

```http
GET /permissions/resources
Authorization: Bearer {token}
```

**Response:**

```json
{
  "success": true,
  "code": 200,
  "meta": {},
  "message": "Resources retrieved successfully",
  "data": [
    {
      "id": "507f1f77bcf86cd799439011",
      "key": "roles",
      "name": "Roles",
      "actions": ["read", "create", "update", "delete"],
      "is_deleted": false,
      "created_at": "2025-10-04T09:36:34.130Z",
      "updated_at": "2025-10-04T09:36:34.130Z"
    }
  ]
}
```

### Get Resource by Key

```http
GET /permissions/resources/{key}
Authorization: Bearer {token}
```

**Example:**

```http
GET /permissions/resources/roles
```

### Update Resource

```http
PUT /permissions/resources/{resource_id}
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "Role Management",
    "actions": ["read", "create", "update", "delete", "assign"]
}
```

**Note:** Updating the name will automatically regenerate the key.

### Delete Resource

```http
DELETE /permissions/resources/{resource_id}
Authorization: Bearer {token}
```

Performs soft delete (sets is_deleted to true).

## Permission Requirements

All resource management endpoints require appropriate permissions:

| Endpoint                           | Required Permission |
| ---------------------------------- | ------------------- |
| POST /permissions/resources        | permissions.create  |
| GET /permissions/resources         | permissions.read    |
| GET /permissions/resources/{key}   | permissions.read    |
| PUT /permissions/resources/{id}    | permissions.update  |
| DELETE /permissions/resources/{id} | permissions.delete  |

## Default Resources

The system initializes with 22 default resources:

1. **users** - User management
2. **roles** - Role management
3. **permissions** - Permission/Resource management
4. **auth** - Authentication
5. **otp** - OTP verification
6. **password** - Password management
7. **students** - Student management
8. **staff** - Staff management
9. **courses** - Course management
10. **departments** - Department management
11. **classrooms** - Classroom management
12. **attendance** - Attendance tracking
13. **exams** - Exam management
14. **fees** - Fee management
15. **library** - Library management
16. **hostel** - Hostel management
17. **transport** - Transport management
18. **canteen** - Canteen management
19. **events** - Event management
20. **timetable** - Timetable management
21. **notifications** - Notification management
22. **reports** - Report generation

## Common Actions

Standard actions used across resources:

- **read** - View/retrieve data
- **create** - Create new records
- **update** - Modify existing records
- **delete** - Remove records

## Usage in Roles

Resources are used in role definitions to specify permissions:

```json
{
  "role": "admin",
  "permissions": [
    {
      "resource": "roles",
      "actions": ["read", "create", "update", "delete"],
      "allowed_actions": ["read", "create", "update", "delete"]
    }
  ]
}
```

## Initialization

Run the initialization script to create default resources and roles:

```bash
python init_roles.py
```

This will:

1. Create all default resources in the database
2. Create default roles (admin, student, teacher)
3. Assign appropriate permissions to each role

## Best Practices

1. **Naming Convention**: Use clear, descriptive names (e.g., "User Management", "Student Records")
2. **Actions**: Keep actions consistent across similar resources
3. **Key Uniqueness**: Keys must be unique; the system prevents duplicates
4. **Soft Delete**: Resources are soft-deleted to maintain referential integrity
5. **Update Carefully**: Changing resource keys affects all roles using that resource

## Integration with Permission System

The permission system automatically uses resources from the database:

```python
# In controllers
@router.get("/")
async def get_items(current_user: dict = Depends(permission_service.require_permission("resource_key", "read"))):
    return {"message": "Success"}
```

The system checks:

1. User's role
2. Role's permissions for the resource
3. If the action is in allowed_actions

## Error Handling

### 400 Bad Request

- Resource with the same key already exists

### 404 Not Found

- Resource not found (may be deleted)

### 403 Forbidden

- User doesn't have required permission

### 500 Internal Server Error

- Database or server error

## Example Workflow

1. **Create a new resource:**

   ```bash
   POST /permissions/resources
   {
       "name": "Grade Management",
       "actions": ["read", "create", "update", "delete"]
   }
   ```

2. **Get the resource key:**

   - Key will be "grade_management"

3. **Update role to include permission:**

   ```bash
   PUT /roles/{role_id}
   {
       "permissions": [
           {
               "resource": "grade_management",
               "actions": ["read", "create", "update", "delete"],
               "allowed_actions": ["read", "create"]
           }
       ]
   }
   ```

4. **Use in controller:**
   ```python
   @router.get("/grades")
   async def get_grades(current_user: dict = Depends(
       permission_service.require_permission("grade_management", "read")
   )):
       return {"grades": []}
   ```
