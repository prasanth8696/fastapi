from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import  OAuth2PasswordBearer
import auth

handler = auth.handler()

protected = [Depends(handler.verify)]
router = APIRouter(
         prefix = '/order',
         tags = ['orders'],
         )





@router.get('/{item_id}')
async def order_item(item_id :int, user=Depends(handler.verify) ) :
  return {'current_user' : user}

