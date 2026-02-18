
import sys
import os

# Add parent directory to path to allow running as script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.controllers import students, assignments, submissions

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stylometric Plagiarism Detection System",
    description="API for detecting plagiarism using stylometry and AI detection.",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(assignments.router)
app.include_router(submissions.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Plagiarism Detection API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
