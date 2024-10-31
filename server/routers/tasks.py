from typing import Annotated

from fastapi import APIRouter, status, Depends

from crud.tasks import TaskService
from schemas.tasks import Task, TaskCreation
from services.auth import access_granted

# Маршрут для действий з задачами
router = APIRouter(prefix='/api/v1/tasks')


# Маршрут для получения всех задач для авторизированных пользователей
@router.get('/', description='Get all tasks', response_model=list[Task],
            status_code=status.HTTP_200_OK, name='get_all_tasks_url',
            responses={200: {'description': 'Успешное получение объектов'},
                       }
            )
async def get_tasks(service: Annotated[TaskService, Depends()],
                    permission: Annotated[bool, Depends(access_granted)], task_status: str = None,):
    if permission:
        result = await service.get_tasks(task_status)
        return result
    else:
        return {'message': 'Авторизуйтесь для получения данных'}


# Маршрут для создания задачи для авторизированных пользователей
@router.post('/', description='Create task',
             response_model=Task,
             status_code=status.HTTP_201_CREATED, name='task_creation_url',
             responses={201: {'description': 'Успешное создание объекта'},
                        409: {'description': 'Объект уже существует'},
                        422: {'description': 'Ошибка валидации данных'}}
             )
async def post_note(data: TaskCreation, permission: Annotated[bool, Depends(access_granted)],
                    service: TaskService = Depends()):
    if permission:
        result = await service.create_task(data)
        return result
    else:
        return {'message': 'Авторизуйтесь для добавления данных'}


# Маршрут для удаления указанной задачи для авторизированных пользователей
@router.delete('/{task_id}', description='Delete task',
               status_code=status.HTTP_201_CREATED, name='task_deletion_url',
               responses={201: {'description': 'Успешное удаление объекта'},
                          404: {'description': 'Объект не найден'},
                          }
               )
async def delete_note(task_id: int, permission: Annotated[bool, Depends(access_granted)],
                      service: TaskService = Depends()) -> dict[str, str]:
    if permission:
        result = await service.delete_task(task_id)
        return result
    else:
        return {'message': 'Авторизуйтесь для удаления данных'}


# Маршрут для изменения задачи для авторизированных пользователей
@router.put('/{task_id}', description='Update task',
            status_code=status.HTTP_200_OK, name='task_updating_url',
            responses={200: {'description': 'Успешное изменение объекта'},
                       404: {'description': 'Объект не найден'},
                       422: {'description': 'Ошибка валидации данных'}
                       }
            )
async def update_note(task_id: int, data: TaskCreation, permission: Annotated[bool, Depends(access_granted)],
                      service: TaskService = Depends()) -> dict[str, str]:
    if permission:
        result = await service.update_task(task_id=task_id, data=data)
        return result
    else:
        return {'message': 'Авторизуйтесь для удаления данных'}


# Маршрут для получения указанной задачи для авторизированных пользователей
@router.get('/{task_id}', description='Get task',
            response_model=Task,
            status_code=status.HTTP_200_OK, name='task_getting_url',
            responses={200: {'description': 'Успешное получение объекта'},
                       404: {'description': 'Объект не найден'},
                       }
            )
async def get_note(task_id: int, permission: Annotated[bool, Depends(access_granted)],
                   service: TaskService = Depends()):
    if permission:
        result = await service.get_task(task_id)
        return result
    else:
        return {'message': 'Авторизуйтесь для удаления данных'}
