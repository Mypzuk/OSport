from fastapi import APIRouter, Depends, HTTPException
from engine import get_db
from datetime import date
from models.ObjectClass import UserBase, ResultsBase
from models.models import Users, Results
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

router = APIRouter()


@router.post('/user/registration')
async def add_user(user: UserBase, db: AsyncSession = Depends(get_db)):
    try:
        # Check if a user with the same id or email already exists
        existing_user = await db.scalar(
            select(Users).where((Users.email == user.email) | (Users.login == user.login))
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь с таким логином или Email уже существует")

        # Add the new user to the database
        db_user = Users(**user.dict())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return {"message": "Пользователь добавлен :3", "user": db_user}
    except HTTPException as e:
        raise e  # Re-raise known HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении пользователя: {str(e)}")


@router.get('/user/login')
async def add_user(login: str, password: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Users).where(Users.login == login, Users.password == password))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return {"message": "Вы успешно авторизовались"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при авторизации пользователя: {str(e)}")

@router.get('/user/{user_id}')
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Users).where(Users.id == user_id))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении пользователя: {str(e)}")


@router.get('/users')
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Users))
        users = result.scalars().all()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении пользователей: {str(e)}")


@router.put('/user/{user_id}/birthdate')
async def update_birth_date(user_id: int, new_birth_date: date, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Users).where(Users.id == user_id))
        user = result.scalar()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        await db.execute(update(Users).where(Users.id == user_id).values(birth_date=new_birth_date))
        await db.commit()
        return {"message": "Дата рождения успешно обновлена!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при обновлении Др: {str(e)}")


@router.delete('/user/{user_id}')
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Users).where(Users.id == user_id))
        user = result.scalar()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        await db.execute(delete(Users).where(Users.id == user_id))
        await db.execute(delete(Results).where(Results.user_id == user_id))
        await db.commit()
        return {"message": "Пользователь успешно удалён!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при удалении: {str(e)}")


@router.get('/user/{user_id}/exists')
async def check_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Users).where(Users.id == user_id))
        if result.first() is None:
            return {"exists": False}
        return {"exists": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при проверке пользователя: {str(e)}")
