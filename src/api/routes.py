"""
Additional API routes (can be used for future expansion).
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/stats")
async def get_stats():
    """Get statistics about the use case database."""
    # This can be implemented to return database statistics
    return {"message": "Stats endpoint - to be implemented"}

