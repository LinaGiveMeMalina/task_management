from fastapi import FastAPI
from task_management.views.tasks import router


app = FastAPI()

app.include_router(router)
