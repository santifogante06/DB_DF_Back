from fastapi import FastAPI
from routers import dashboard
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Dashboard API. Use /dashboard for dashboard operations."}