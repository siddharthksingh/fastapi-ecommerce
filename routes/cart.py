from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from database import db
from utils import verify_token, require_roles

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.put("/add")
@require_roles(["admin", "user"])
async def add_to_cart(product_id: str, user: dict = Depends(verify_token)):
    """Add a product to the user's cart (stored in the user model)."""
    email = user["email"]

    # Check if product exists in the database
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Find user in DB
    user_data = await db.users.find_one({"email": email})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    cart = user_data.get("cart", {})

    # If product is already in cart, increment quantity
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    # Update the user's cart (append product to the cart list)
    await db.users.update_one(
        {"email": email},
        {"$set": {"cart": cart}}
    )

    return {"message": "Product added to cart"}


@router.get("/get")
@require_roles(["admin", "user"])
async def get_cart(user: dict = Depends(verify_token)):
    """Retrieve the user's cart (stored in the user model)."""
    email = user["email"]

    # Find user in DB
    user_data = await db.users.find_one({"email": email})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    cart = user_data.get("cart", {})

    # Fetch product details from the database
    product_ids = [ObjectId(pid) for pid in cart.keys()]
    products = await db.products.find({"_id": {"$in": product_ids}}).to_list(length=None)

    # Format cart response
    cart_items = [
        {
            "product_id": str(product["_id"]),
            "name": product["name"],
            "cost": product["cost"],
            "quantity": cart[str(product["_id"])]
        }
        for product in products
    ]

    return {"cart": cart_items}

@router.put("/remove")
@require_roles(["admin", "user"])
async def remove_from_cart(product_id: str, user: dict = Depends(verify_token)):
    """Remove a product from the user's cart (stored in the user model)."""
    email = user["email"]

    # Find user in DB
    user_data = await db.users.find_one({"email": email})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    cart = user_data.get("cart", {})

    # Check if product exists in the cart
    if product_id not in cart:
        raise HTTPException(status_code=404, detail="Product not found in cart")
    else:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            cart.pop(product_id)

    # Update the user's cart (append product to the cart list)
    await db.users.update_one(
        {"email": email},
        {"$set": {"cart": cart}}
    )

    return {"message": "Product removed from cart"}