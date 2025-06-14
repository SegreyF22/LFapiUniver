from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from api.handlers import user_router
from api.login_handler import login_router

# Создание приложения FastApi
app = FastAPI(title="LFApiUniver")

# Главный роутер, который будет собирать в себя остальные роутеры
main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])# передаем в гл.роутер user_router
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(main_api_router) # передаем в наше приложение те роутеры, которые создали

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)