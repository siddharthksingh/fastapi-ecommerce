from fastapi import APIRouter, Depends, HTTPException
from models.product import Product, ProductUpdate
from database import db
from utils import verify_token, require_roles
from bson import ObjectId

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/add", response_model=Product)
@require_roles(["admin"])
async def add_product(product: Product, user: dict = Depends(verify_token)):
    new_product = product.model_dump()
    result = await db.products.insert_one(new_product)
    return {**new_product, "id": str(result.inserted_id)}


@router.get("/get", response_model=dict[str, list])
@require_roles(["admin", "user"])
async def get_products(user: dict = Depends(verify_token)):
    products = await db.products.find().to_list(None)

    products_list = [
        {
            "_id": str(product["_id"]),  # Convert ObjectId to string
            "name": product["name"],
            "cost": product["cost"],
            "quantity": product["quantity"]
        }
        for product in products
    ]

    return {"products": products_list}


@router.put("/update")
@require_roles(["admin"])
async def update_product(product_id: str, update_data: ProductUpdate, user: dict = Depends(verify_token)):
    """Update product information."""

    # Check if product exists in the database
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_fields = {k: v for k, v in update_data.model_dump().items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    await db.products.update_one({"_id": ObjectId(product_id)}, {"$set": update_fields})

    return {"message": "Product information updated successfully", "updated_fields": update_fields}
