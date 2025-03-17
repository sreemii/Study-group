from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import JSONResponse
from models import Base
from database import engine
from routes import auth, users, groups, sessions, resources

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include all routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(groups.router, prefix="/groups", tags=["Groups"])
app.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
app.include_router(resources.router, prefix="/resources", tags=["Resources"])

# Root route to check if API is running
@app.get("/")
def read_root():
    return {"message": "API is running!"}

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def catch_all(full_path: str):
    raise HTTPException(status_code=404, detail="This endpoint does not exist")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "An internal error occurred", "details": str(exc)},
    )