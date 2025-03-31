from fastapi import FastAPI
import uvicorn
from routes import auth, products, cart, orders

app = FastAPI(title="Minimal eCommerce API")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the eCommerce API!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)