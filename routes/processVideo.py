from fastapi import UploadFile, File, APIRouter
import shutil
import os

from cv.squats import check_squats
from cv.push_ups import check
from cv.climber import check_climber
from cv.bicycle import check_bicycle
from cv.pull_ups import check_pull


router = APIRouter()


@router.post("/pushUps")
async def push_ups(video: UploadFile = File(...)):
    try:
        with open(f"cv/cvmedia/{video.filename}", "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        count =  await check(video.filename)

        os.remove(f"cv/cvmedia/{video.filename}")
        return count
    except Exception as e:
        return {"error": f"Произошла ошибка при загрузке файла: {str(e)}"}
    

@router.post("/squats")
async def squats(video: UploadFile = File(...)):
    try:
        with open(f"cv/cvmedia/{video.filename}", "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        count = await check_squats(video.filename)

        os.remove(f"cv/cvmedia/{video.filename}")
        return count
    except Exception as e:
        return {"error": f"Произошла ошибка при загрузке файла: {str(e)}"}


@router.post("/climber")
async def climber(video: UploadFile = File(...)):
    try:
        with open(f"cv/cvmedia/{video.filename}", "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        count = await check_climber(video.filename)

        os.remove(f"cv/cvmedia/{video.filename}")
        return count
    except Exception as e:
        return {"error": f"Произошла ошибка при загрузке файла: {str(e)}"}
    
@router.post("/bicycle")
async def bicycle(video: UploadFile = File(...)):
    try:
        with open(f"cv/cvmedia/{video.filename}", "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        count = await check_bicycle(video.filename)

        os.remove(f"cv/cvmedia/{video.filename}")
        return count
    except Exception as e:
        return {"error": f"Произошла ошибка при загрузке файла: {str(e)}"}
    
@router.post("/pullUps")
async def pull_ups(video: UploadFile = File(...)):
    try:
        with open(f"cv/cvmedia/{video.filename}", "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        count = await check_pull(video.filename)

        os.remove(f"cv/cvmedia/{video.filename}")
        return count
    except Exception as e:
        return {"error": f"Произошла ошибка при загрузке файла: {str(e)}"}