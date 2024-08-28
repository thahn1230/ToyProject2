from fastapi import APIRouter, Depends, HTTPException 
from fastapi.responses import JSONResponse

from app.crud.score_crud import *

router = APIRouter()