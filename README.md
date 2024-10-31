# Тестовое приложение для управления списком задач
 
_* Скопируйте проект к себе на ПК при помощи: git clone https://github.com/ConstCK/Beresnev-Test.git
* Перейдите в папку проекта
* Создайте файл .env в каталоге проекта и пропишите в нем настройки по примеру .env.example_

## Важно:
1. **На ПК должно быть установлен и запушен DockerDesktop !
2. Запустите сервер из каталога проекта командой "docker-compose up"
3. Для запросов к серверу используйте Swagger или Postman**

EndPoints:
* http://localhost:8000/docs/ - Документация к API (Swagger)
* http://localhost:8000/redoc/ - Документация к API (Альтернативный вариант)
* http://localhost:8080 - Доступ к панели администрирования БД
* 
* http://localhost:8000/api/v1/auth - Маршруты с авторизацией
* http://localhost:8000/api/v1/tasks - Маршруты с задачами



