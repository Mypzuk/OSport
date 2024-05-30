from fastapi import APIRouter, Depends, HTTPException, status
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from models.ObjectClass import UserBase, ResultsBase
from models.models import Users, Results
from engine import get_db

router = APIRouter()

# Add a new user
@router.post('/userAdd')
async def add_user(user: UserBase, db: AsyncSession = Depends(get_db)):
    try:
        db_user = Users(**user.dict())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return {"message": "Пользователь добавлен :3"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении пользователя: {str(e)}")

# Get a user by telegram_id
@router.get('/getUser')
async def get_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    try:
        results = await db.execute(select(Users).where(Users.telegram_id == telegram_id))
        user = results.scalar()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении пользователя: {str(e)}")

# Get all users
@router.get('/getUsers')
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        results = await db.execute(select(Users))
        users = results.scalars().all()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении пользователей: {str(e)}")

# Update birth date of a user
@router.put('/updateBirthDate')
async def update_birth_date(telegram_id: int, new_birth_date: date, db: AsyncSession = Depends(get_db)):
    try:
        user = await db.scalar(select(Users).where(Users.telegram_id == telegram_id))
        if user is None:
            raise HTTPException(status_code=404, detail="Такого пользователя нет")

        query = update(Users).where(Users.telegram_id == telegram_id).values(birth_date=new_birth_date)
        await db.execute(query)
        await db.commit()
        return {"message": "Дата рождения успешно обновлена!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при обновлении даты рождения: {str(e)}")

# Delete a user by telegram_id
@router.delete('/deleteUser')
async def delete_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await db.scalar(select(Users).where(Users.telegram_id == telegram_id))
        if user is None:
            raise HTTPException(status_code=404, detail="Такого пользователя нет")

        # Delete user from Users table
        await db.execute(delete(Users).where(Users.telegram_id == telegram_id))

        # Delete user from Results table
        await db.execute(delete(Results).where(Results.user_id == user.id))

        await db.commit()
        return {"message": "Пользователь успешно удалён!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при удалении: {str(e)}")

# Check if a user exists by telegram_id
@router.get('/checkUser')
async def check_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await db.scalar(select(Users).where(Users.telegram_id == telegram_id))
        return user is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при проверке пользователя: {str(e)}")
