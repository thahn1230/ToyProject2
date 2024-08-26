from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from app.routers.user_routers import router as user_routers


app = FastAPI()

# Favicon Static
# Get rid of favicon.ico 404 Not Found error
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_routers)

@app.get('/')
async def home(request: Request):
    domain = request.headers.get("host")
    return {"message": f"Hello from {domain}"}