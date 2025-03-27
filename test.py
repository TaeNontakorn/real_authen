from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt
import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # URL ของ Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)



SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

class AuthRequest(BaseModel):
    client_id: str
    client_secret: str

# ฐานข้อมูลจำลองของ client และ role
clients_db = {
    "bosskung": {"client_secret": "123456", "role": "member"},
    "bossmiao": {"client_secret": "123456", "role": "member"},
    "bosstae": {"client_secret": "123456", "role": "member"},
    "guest": {"client_secret": "123", "role": "guest"},
}

def create_jwt_token(data: dict, expires_delta: int):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/auth")
def authenticate(auth: AuthRequest):
    client = clients_db.get(auth.client_id)
    if client and client["client_secret"] == auth.client_secret:
        token = create_jwt_token({"sub": auth.client_id, "role": client["role"]}, expires_delta=10)
        return {"access_token": token, "role": client["role"]}
    raise HTTPException(status_code=401, detail="Invalid credentials")
