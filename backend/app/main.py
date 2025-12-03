from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import jobs, resumes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Match Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router)
app.include_router(resumes.router)


@app.get("/")
def healthcheck():
    return {"status": "ok"}





