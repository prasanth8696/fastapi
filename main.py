from fastapi import FastAPI
from router1 import router
from database import engine
import models
import home
import admin
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(home.home)
app.include_router(router)
#app.include_router(order.router)
app.include_router(admin.Admin)

