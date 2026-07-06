"""Central API router aggregation.

Every module (users, movies, auditoriums, reservations, ...) exposes its own
APIRouter. This module bundles them into a single `api_router` that main.py
mounts under the API_V1_STR prefix.

HOW TO ADD A MODULE ONCE IT HAS ENDPOINTS:

    from src.users.router import router as users_router

    api_router.include_router(
        users_router,
        prefix="/users",
        tags=["users"],
    )

Right now none of the modules define a router yet, so this aggregator is
intentionally empty. Wire each one in as you build its endpoints.
"""

from fastapi import APIRouter

api_router = APIRouter()

# --- Register module routers here as they are implemented ---
# api_router.include_router(users_router, prefix="/users", tags=["users"])
# api_router.include_router(movies_router, prefix="/movies", tags=["movies"])
# api_router.include_router(auditoriums_router, prefix="/auditoriums", tags=["auditoriums"])
# api_router.include_router(reservations_router, prefix="/reservations", tags=["reservations"])
