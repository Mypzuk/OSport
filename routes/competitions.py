from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from models.ObjectClass import CompetitionBase
from models.models import Competitions, Results
from engine import get_db

router = APIRouter()

# Добавление соревнования
@router.post('/addCompetition')
async def add_competition(competition: CompetitionBase, db: AsyncSession = Depends(get_db)):
    try:
        db_competition = Competitions(**competition.dict())
        db.add(db_competition)
        await db.commit()
        await db.refresh(db_competition)
        return {"message": "Соревнование добавлено :3"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении: {str(e)}")

# Удаление определённого соревнования
@router.delete('/deleteCompetition')
async def delete_competition(competition_id: int, db: AsyncSession = Depends(get_db)):
    try:
        competition = await db.execute(select(Competitions).where(Competitions.competition_id == competition_id))
        checkCompetition = competition.scalar()
        if checkCompetition is None:
            raise HTTPException(status_code=404, detail="Такого соревнования нет")

        await db.execute(delete(Competitions).where(Competitions.competition_id == competition_id))
        await db.execute(delete(Results).where(Results.competition_id == competition_id))
        await db.commit()
        return {"message": "Соревнование удалено :3"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при удалении: {str(e)}")

# Изменение определённого соревнования
@router.put('/editCompetition')
async def edit_competition(competition_id: int, competition: CompetitionBase, db: AsyncSession = Depends(get_db)):
    try:
        db_competition = await db.get(Competitions, competition_id)
        if db_competition is None:
            raise HTTPException(status_code=404, detail="Такого соревнования нет")

        for field, value in competition.dict().items():
            setattr(db_competition, field, value)
        await db.commit()
        return {"message": "Соревнование обновлено :3"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при обновлении: {str(e)}")

# Выборка id первого соревнования в БД
@router.get('/getFirstId')
async def get_first_id(db: AsyncSession = Depends(get_db)):
    try:
        query = select(Competitions.competition_id).order_by(Competitions.competition_id.asc())
        result = await db.execute(query)
        first_id = result.scalar()
        if first_id is None:
            raise HTTPException(status_code=404, detail="Соревнования не найдены")
        return {"competition_id": first_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении данных: {str(e)}")

# Выборка определённого соревнования
@router.get('/getCompetition')
async def get_competition(competition_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Competitions).where(Competitions.competition_id == competition_id)
        result = await db.execute(query)
        competition = result.scalar()
        if competition is None:
            raise HTTPException(status_code=404, detail="Соревнование не найдено")
        return competition
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении данных: {str(e)}")

# Выборка всех соревнований
@router.get('/getAllCompetition')
async def get_all_competition(db: AsyncSession = Depends(get_db)):
    try:
        query = select(Competitions)
        result = await db.execute(query)
        competitions = result.scalars().all()
        return {"competitions": competitions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при получении данных: {str(e)}")
