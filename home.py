from fastapi import APIRouter
from database import sessionlocal
from models import items
session = sessionlocal()

home = APIRouter(
                 tags = ['HOME'])


@home.get('/',status_code=200)
async def get_items():
  items_values = session.query(items).all()
  return items_values
