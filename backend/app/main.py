from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import prospect  # noqa: F401
from app.models import conversation  # noqa: F401
from app.models import message  # noqa: F401
from app.models import utilisateur  # noqa: F401
from app.routers import auth



from app.routers import chatbot
from app.routers import prospect as prospect_router
from app.routers import conversation as conversation_router
from app.routers import dashboard as dashboard_router

app = FastAPI(
    title="Taysir Chatbot API",
    description="Assistant conversationnel intelligent de qualification des prospects"
)

Base.metadata.create_all(bind=engine)

app.include_router(chatbot.router)
app.include_router(prospect_router.router)
app.include_router(conversation_router.router)
app.include_router(dashboard_router.router)
app.include_router(auth.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Taysir Chatbot API"
    }
