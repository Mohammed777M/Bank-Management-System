from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore

app = FastAPI()

# Dummy database
db = {
    1: {"name": "Alice", "number": "1234567890", "balance": 1000}
}

class User(BaseModel):
    name: str
    number: str
    balance: float

# ✅ PUT: update a user
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")

    db[user_id] = user.dict()
    return {"message": "User updated", "user": db[user_id]}

# ✅ DELETE: delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")

    del db[user_id]
    return {"message": f"User {user_id} deleted successfully"}
