from fastapi import FastAPI
from app.routes.category_routes import category_router

app = FastAPI()

@app.get("/health-check")
async def health_check():
    return True


app.include_router(category_router)