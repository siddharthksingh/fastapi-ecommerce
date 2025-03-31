from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from database import db
from utils import verify_token, require_roles

router = APIRouter(prefix="/orders", tags=["Order"])

@router.post("/order")
@require_roles(["admin", "user"])
async def place_order(user: dict = Depends(verify_token)):
    """Purchase items in cart"""
    email = user["email"]
    user_data = await db.users.find_one({"email": email})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    cart = user_data.get("cart", {})

    product_ids = [ObjectId(pid) for pid in cart.keys()]

    # ✅ Step 2: Fetch product details
    products = await db.products.find({"_id": {"$in": product_ids}}).to_list(None)

    if len(products) != len(cart):
        raise HTTPException(status_code=400, detail="One or more products not found")

    # ✅ Step 3: Verify stock availability & Calculate total cost
    total_cost = 0
    update_operations = []

    for product in products:
        product_id = str(product["_id"])
        ordered_quantity = cart[product_id]

        if product["quantity"] < ordered_quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product_id}. Available: {product['quantity']}"
            )

        total_cost += product["cost"] * ordered_quantity

        # Prepare update operation to deduct stock
        update_operations.append(
            {
                "filter": {"_id": product["_id"]},
                "update": {"$inc": {"quantity": -ordered_quantity}}
            }
        )

    # ✅ Step 4: Deduct stock using bulk write
    if update_operations:
        from pymongo import UpdateOne
        await db.products.bulk_write([UpdateOne(op["filter"], op["update"]) for op in update_operations])

    # ✅ Step 5: Save order in `orders` collection
    order = {
        "user_email": email,
        "items": [{"product_id": pid, "quantity": qty} for pid, qty in cart.items()],
        "total_cost": total_cost
    }
    result = await db.orders.insert_one(order)

    # ✅ Step 6: Clear the user's cart after placing the order
    await db.users.update_one({"email": email}, {"$set": {"cart": {}}})

    return {"message": "Order placed successfully", "order_id": str(result.inserted_id)}