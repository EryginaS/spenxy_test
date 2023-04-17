from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers.activity_accouting import router as report_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(report_router, tags=['default_values'])
