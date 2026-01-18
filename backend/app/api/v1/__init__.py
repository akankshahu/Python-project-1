from fastapi import APIRouter
from app.api.v1.endpoints import drugs, clinical_trials, analytics

api_router = APIRouter()

api_router.include_router(drugs.router)
api_router.include_router(clinical_trials.router)
api_router.include_router(analytics.router)
