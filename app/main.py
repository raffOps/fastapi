from fastapi import FastAPI
from app.routes.category_routes import category_router
from app.routes.product_routes import product_router
from app.routes.user_routes import user_routes

app = FastAPI()

@app.get("/health-check")
async def health_check():
    return True


app.include_router(category_router)
app.include_router(product_router)
app.include_router(user_routes)
