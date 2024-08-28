from fastapi import APIRouter, Depends, HTTPException 
from fastapi.responses import JSONResponse

from app.crud.user_crud import *

router = APIRouter()

@router.post("/user/check_user_info")
async def check_user_info(params: dict):
    id = params["id"]
    result = check_user_df(id=id)

    if result != False:
        return JSONResponse({
            "result" : True,
            "user_info" : result
            })
    else:    
        return JSONResponse({"result" : False})

@router.post("/user/sign_up")
async def register_user(params: dict):
    result = sign_up(params)
    if result: 
        return JSONResponse({"result" : True})
    else :
        return JSONResponse({"result" : False})

@router.post("/user/modify_user")
async def modify_user(params: dict):
    result = modify_user_info(params)
    if result: 
        return JSONResponse({"result" : True})
    else :
        return JSONResponse({"result" : False})