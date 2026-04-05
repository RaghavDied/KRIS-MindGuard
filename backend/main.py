from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.predict import predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "db.json"

class User(BaseModel):
    username: str
    password: str

class TextInput(BaseModel):
    text: str
    username: str 


def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": []}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.get("/")
def home():
    return {"message": "Mental Health & Toxicity API is running 🚀"}


@app.post("/signup")
def signup(user: User):
    db = load_db()

    for u in db["users"]:
        if u["username"] == user.username:
            return {"error": "User already exists"}

    db["users"].append({
        "username": user.username,
        "password": user.password,
        "history": []
    })

    save_db(db)
    return {"message": "User created successfully"}

@app.post("/login")
def login(user: User):
    db = load_db()

    for u in db["users"]:
        if u["username"] == user.username and u["password"] == user.password:
            return {
                "message": "Login successful",
                "history": u["history"]
            }

    return {"error": "Invalid credentials"}

@app.post("/predict")
def get_prediction(input: TextInput):
    result = predict(input.text)
    result["text"] = input.text

    db = load_db()


    for u in db["users"]:
        if u["username"] == input.username:
            u["history"].append(result)

    save_db(db)

    return result