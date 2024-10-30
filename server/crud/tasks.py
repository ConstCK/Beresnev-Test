from fastapi import Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from schemas.tasks import Task, TaskCreation
from models.models import Task as TaskTable


class TaskService:
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.db = session

    # Получение всех задач
    async def get_tasks(self, task_status: str = None) -> list[Task]:
        if not status:
            query = select(TaskTable)
            result = await self.db.execute(query)
        else:
            query = select(TaskTable).where(TaskTable.status == task_status)
            result = await self.db.execute(query)

        return result.scalars().all()

    # Создание задачи
    async def create_task(self, data: TaskCreation) -> Task:
        try:
            query = insert(TaskTable).values(**data.model_dump()).returning(TaskTable)
            result = await self.db.execute(query)
            await self.db.flush()
            result = Task.model_validate(result.scalar())
            await self.db.commit()
            return result
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Ошибка при создании задачи.'
                                                                         ' Проверьте введенные данные.')

    # Получение указанной задачи
    async def get_task(self, task_id: int) -> Task:
        try:
            query = select(TaskTable).where(TaskTable.id == task_id)
            result = await self.db.execute(query)
            task = Task.model_validate(result.scalar())
            return task
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Объект не существует')

    # Изменение указанной задачи
    async def update_task(self, task_id: int, data: TaskCreation, ) -> dict[str, str]:
        try:
            query = select(TaskTable).where(TaskTable.id == task_id)

            result = await self.db.execute(query)
            task = result.scalar()
            task.name = data.name
            task.description = data.description
            task.status = data.status
            await self.db.commit()
            return {'message': f'Задача №{task_id} успешно обновлена'}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Ошибка обновления объекта')

    # Удаление указанной задачи
    async def delete_task(self, task_id: int) -> dict[str, str]:
        try:
            query = select(TaskTable).where(TaskTable.id == task_id)
            result = await self.db.execute(query)
            await self.db.delete(result.scalar())
            return {'message': f'Задача №{task_id} успешно удалена'}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Объект для удаления не найден')
