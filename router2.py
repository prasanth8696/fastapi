from fastapi import APIRouter,HTTPException,Depends
from models import orders,Users
from database import sessionlocal
import auth
session = sessionlocal()

handler = auth.handler()
protected = Depends(handler.verify)
order = APIRouter(
         prefix = '/order',
         tags = ['Orders'] )



#post the order

@order.get('/place_order/{item_id}',status_code = 201) :
def place_order(request: OrderModel,payload = protected) :

  username =  payload['sub']
  current_user = session.query(Users).filter(Users.username == username).first()
  new_order = orders(
           	)
