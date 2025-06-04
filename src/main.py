from dotenv import find_dotenv, load_dotenv
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from src.database import get_database, add_product, get_all_items, add_user, find_user, delete_item


# Global variables and env variables loading
load_dotenv()

# Define the Pydantic model for an item
class Item(BaseModel):
    nome: str
    prezzo: float
    timestamp: str
    category: str  # New field for item category

# Define the Pydantic model for a user
class User(BaseModel):
    name: str
    surname: str
    age: int


# Use FastAPI lifespan event handler
@asynccontextmanager
async def lifespan(app : FastAPI) :

    global db
    db = get_database()

    if db is None:
        raise RuntimeError("Database connection failed!")
    yield


app = FastAPI(lifespan = lifespan)



@app.get("/")
async def read_root():
    return {"message": "Hello User!"}



@app.get("/user")
async def get_user(name: str = None):

    if name is not None:
        message = f"Hello {name}!"
    else:
        message = f"Hello World!"
    

    return {"message": message}


@app.get("/items")
async def list_items():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")
    items = get_all_items(db)
    return items


@app.post("/addItem")
async def create_item(item: Item):

    # item = Item(
    #     nome = "cazzo di item",
    #     prezzo = 0.50,
    #     timestamp = "eterno"
    # )

    if db is None :
        raise HTTPException(
            status_code = 500,
            detail = "Database not available"
        )
    
    add_product(
        db,
        item.model_dump()
    )

    return {"message": "Item added successfully"}


@app.post("/addUser")
async def create_user(user: User):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")
    result = add_user(db, user.model_dump())
    if result:
        return {"message": "User added or already exists", "user": result}
    else:
        raise HTTPException(status_code=500, detail="Failed to add user")


@app.get("/findUser")
async def get_user_by_name(name: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")
    user = find_user(db, name)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete("/deleteItem")
async def remove_item(nome: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")
    success = delete_item(db, nome)
    if success:
        return {"message": f"Item '{nome}' deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items/by_category")
async def list_items_by_category(category: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")
    from src.database import get_items_by_category
    items = get_items_by_category(db, category)
    return items


@app.get("/indices")
async def get_indices():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")
    from src.database import get_mean_price_by_category
    mean_price_by_category = get_mean_price_by_category(db)
    return {
        "mean_price_by_category": mean_price_by_category
    }





