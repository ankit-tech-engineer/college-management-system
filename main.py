from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from config.database import connect_db
from routes.api_router import api_router
from config.settings import APP_NAME, VERSION
from modules.auth.dependencies import AuthException
from modules.permissions.permissionService import PermissionService
from core.response import create_response
from libs.middleware import RequestLoggerMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="College Management System API",
    lifespan=lifespan
)

# Exception handlers
@app.exception_handler(AuthException)
async def auth_exception_handler(request: Request, exc: AuthException):
    return JSONResponse(
        status_code=exc.code,
        content=create_response(
            success=False,
            code=exc.code,
            message=exc.message,
            data=None
        )
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logger middleware
app.add_middleware(RequestLoggerMiddleware)

# Include routers

@app.get("/")
async def root():
    return {
        "message": "College Management System API",
        "version": VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)