from app.db.session_handler import Base, engine
from fastapi import FastAPI
from app.routes.api import router
from app.core.load_moke_data import load_users_to_redis

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Alert service",
    debug=True,
    version="0.1"
)


@app.on_event("startup")
async def startup_event():
    load_users_to_redis()


@app.get("/")
def root():
    return {"Message": "Root worked"}


app.include_router(router)