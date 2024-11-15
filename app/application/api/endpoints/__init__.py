from .apply import router as apply_router
from .org import router as org_router
from .user import router as user_router

routers = (apply_router, org_router, user_router)
