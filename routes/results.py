from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, and_, desc, func

from models.ObjectClass import ResultsBase
from models.models import Results, Users, Competitions
from engine import get_db

router = APIRouter()

# Add a result to the database
@router.post('/result/add')
async def add_result(result: ResultsBase, db: AsyncSession = Depends(get_db)):
    try:
        user = await db.scalar(select(Users).where(Users.id == result.user_id))
        if user is None:
            raise HTTPException(status_code=404, detail="Такого пользователя нет")

        competition = await db.scalar(select(Competitions).where(Competitions.competition_id == result.competition_id))
        if competition is None:
            raise HTTPException(status_code=404, detail="Такого соревнования нет")

        db_result = Results(**result.dict())
        db.add(db_result)
        await db.commit()
        await db.refresh(db_result)
        return {"message": "Результат добавлен :3", "result": db_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении: {str(e)}")

# Edit user result for a specific competition
@router.put('/result/edit')
async def edit_result(data: ResultsBase, db: AsyncSession = Depends(get_db)):
    try:
        query = update(Results).where(
            and_(Results.competition_id == data.competition_id, Results.user_id == data.user_id)
        ).values(video=data.video, count=data.count, status=data.status)
        await db.execute(query)
        await db.commit()
        return {"message": "Результат изменен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при изменении: {str(e)}")

# Nullify the count of repetitions
@router.post('/result/nullify')
async def set_null_result(result_id: str, db: AsyncSession = Depends(get_db)):
    try:
        query = update(Results).where(Results.result_id == result_id).values(count=None)
        await db.execute(query)
        await db.commit()
        return {"message": "Результат обнулен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при обнулении: {str(e)}")

# Edit the count of repetitions
@router.post('/result/edit-сount')
async def edit_count_result(result_id: str, new_count: str, db: AsyncSession = Depends(get_db)):
    try:
        query = update(Results).where(Results.result_id == result_id).values(count=new_count, status="✅")
        await db.execute(query)
        await db.commit()
        return {"message": "Результат повторений обновлен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при обновлении: {str(e)}")

# Delete a user result
@router.delete('/result/{result_id}')
async def delete_result(result_id: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.scalar(select(Results).where(Results.result_id == result_id))
        if result is None:
            raise HTTPException(status_code=404, detail="Такого результата нет")
        
        await db.execute(delete(Results).where(Results.result_id == result_id))
        await db.commit()
        return {"message": "Результат удален"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при удалении: {str(e)}")

# Get all results for a specific user
@router.get('/user/{user_id}/results')
async def get_user_all(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        results = await db.scalars(select(Results).where(Results.user_id == user_id))
        return results.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении данных: {str(e)}")

# Get user result for a specific competition
@router.get('/user/{user_id}/competition/{competition_id}/result')
async def get_user_result(user_id: str, competition_id: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.scalar(select(Results).where(and_(Results.user_id == user_id, Results.competition_id == competition_id)))
        if result is None:
            raise HTTPException(status_code=404, detail="Результат не найден")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении данных: {str(e)}")

# Get all results from the database
@router.get('/results')
async def get_all_result(db: AsyncSession = Depends(get_db)):
    try:
        results = await db.scalars(select(Results))
        return results.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении данных: {str(e)}")

# Get all results for a specific competition
@router.get('/competition/{competition_id}/results')
async def get_competition_result(competition_id: str, db: AsyncSession = Depends(get_db)):
    try:
        results = await db.scalars(select(Results).where(Results.competition_id == competition_id))
        return results.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении данных: {str(e)}")

# Get user IDs for all participants in a specific competition
@router.get('/competition/{competition_id}/participants')
async def get_competition_members(competition_id: str, db: AsyncSession = Depends(get_db)):
    try:
        user_ids = await db.scalars(select(Results.user_id).where(Results.competition_id == competition_id))
        return user_ids.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении данных: {str(e)}")

# Check the status of a user's result for a specific competition
@router.get('/competition/{competition_id}/user/{user_id}/status')
async def check_status(competition_id: str, user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        statuses = await db.scalars(select(Results.status).where(and_(Results.competition_id == competition_id, Results.user_id == user_id)))
        if statuses is None:
            raise HTTPException(status_code=404, detail="Статус не найден")
        return statuses.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении данных: {str(e)}")

# Filter competition results by count in descending order
@router.get('/competition/{competition_id}/rating')
async def rating_users(competition_id: str, db: AsyncSession = Depends(get_db)):
    try:
        results = await db.scalars(
            select(Results)
            .where(Results.competition_id == competition_id)
            .filter(Results.count.isnot(None))
            .order_by(desc(Results.count))
        )
        return results.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении данных: {str(e)}")

# Global rating for all users based on the total count
@router.get('/rating')
async def total_rating_users(db: AsyncSession = Depends(get_db)):
    try:
        total_counts = await db.execute(
            select(Results.user_id, func.sum(Results.count).label('total_count'))
            .filter(Results.status.isnot(None), Results.count > 0)
            .group_by(Results.user_id)
            .order_by(desc(func.sum(Results.count)))
        )
        return total_counts.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении данных: {str(e)}")


@router.get('/user/{user_id}/competitions')
async def competition_info(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        competitions = await db.execute(
            select(
                Results.competition_id,
                Competitions.title,
                Results.count
            )
            .join(Competitions, Results.competition_id == Competitions.competition_id)
            .where(Results.user_id == user_id)
            .group_by(Results.competition_id, Competitions.title)
        )


        competition_data = []
        for row in competitions:
            competition_id, title, user_count = row
            
            # Get total participants in the competition
            members = await db.scalar(
                select(func.count(Results.user_id)).where(Results.competition_id == competition_id)
            )
            
            # Get user's place by count
            subquery = select(
            Results,
            func.row_number().over(order_by=Results.count.desc()).label('row_number')).filter(Results.competition_id == competition_id).subquery()

            # Основной запрос
            query = select(subquery.c.row_number).filter(subquery.c.user_id == user_id)
        
            # Выполнение запроса
            result = await db.execute(query)
            user_place = result.scalar()
            
            # Get the competition end date
            end_date = await db.scalar(
                select(Competitions.end_date).where(Competitions.competition_id == competition_id)
            )
            
            competition_data.append({
                "title": title,
                "count": user_count,
                "members": members,
                "place": user_place,
                "end_date": end_date
            })
        
        return competition_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении данных: {str(e)}")
