# College Management System Backend

A comprehensive FastAPI-based backend system for managing college operations with role-based access control, student admissions, and various administrative modules.

## 🚀 Quick Start with Docker (Recommended)

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with your credentials

# 3. Start with Docker
make build
make up

# 4. Access API at http://localhost:5000
```

📖 **Detailed Docker Guide**: See [DOCKER_SUMMARY.md](DOCKER_SUMMARY.md)

## 📋 Features

- ✅ Complete Authentication System (JWT + OTP)
- ✅ Role-Based Access Control (36 resources)
- ✅ Student Admission Workflow
- ✅ File Upload (Cloudinary)
- ✅ Email Notifications
- ✅ Master Data Management
- ✅ Request Logging
- ✅ Dockerized Setup

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.115.2
- **Database**: MongoDB (Motor async)
- **Authentication**: JWT + OAuth2
- **File Storage**: Cloudinary
- **Email**: SMTP
- **Containerization**: Docker + Docker Compose

## 📦 Installation

### Option 1: Docker (Recommended)

See [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)

### Option 2: Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Initialize roles
python init_roles.py

# Run server
python main.py
```

## 📚 Documentation

- [Docker Summary](DOCKER_SUMMARY.md) - Complete Docker guide
- [Permission System](PERMISSION_SYSTEM.md) - RBAC documentation
- [Resource Management](RESOURCE_MANAGEMENT.md) - Resource system

## 🔗 API Endpoints

- **API Docs**: http://localhost:5000/docs
- **Health Check**: http://localhost:5000/health
- **Base URL**: http://localhost:5000/api/v1

## 👥 Default Roles

- **Super Admin**: Full access
- **Admin**: Administrative access
- **Student**: Read-only access
- **Teacher**: Teaching operations

## 📞 Support

For issues or questions, check the documentation files or review container logs:
```bash
make logs
``` 
