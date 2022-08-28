from fastapi import APIRouter,HTTPException,Depends
from models import users,orders,items
from database import sessionlocal
import auth
from schemas import ItemModel,UpdateModel
handler = auth.handler()
session = sessionlocal()
protected = Depends(handler.verify)

Admin = APIRouter(
        prefix = '/admin',
        tags = ['ADMIN']
       )

def authorize(current_user):
  if  current_user['owner'] or  current_user['admin'] :
     return
  else :
    raise HTTPException(status_code=401,detail='your dont have enough permission!')

def check_owner(current_user):
  if not current_user['owner'] :
    raise HTTPException(status_code=401,detail='un authorized')
  else :
   return

def discount(price,discount):
  discount = price * discount/100
  return price - discount
#create items
@Admin.post('/post_items',status_code=201)
async def post_item(item : ItemModel,payload = protected) :
  #check user is admin or not
  authorize(payload)

  curr_item = session.query(items).filter(items.name == item.name).first()
  if curr_item is not None :
    raise HTTPException(status_code=400,detail='item already Found')
  new_item = items(
         name = item.name,
         discount = item.discount,
         original_price = item.price
       )
  if item.discount > 0 :
     discounted_price = discount(item.price,item.discount)
     new_item.discounted_price = discounted_price
  else :
    new_item.discounted_price = item.price
  session.add(new_item)
  session.commit()
  session.refresh(new_item)
  return new_item

#get all items
@Admin.get('/items',status_code=200)
async def get_itmes(payload = protected) :
  authorize(payload)
  item_values = session.query(items).all()
  return item_values


#update items
@Admin.put('/update_items',status_code=201)
async def update_items(request:UpdateModel,payload = protected) :
  authorize(payload)
  item = session.query(items).filter(request.id ==items.id).first()
  item.discount = request.discount
  item.quantity = request.quantity
  if request.discount > 0 :
    discounted_price =  discount(item.original_price,request.discount)
    item.discounted_price = discounted_price
  else :
    discounted_price = item.original_price

  session.commit()
  return {'msg' : 'Upadted successfully'}


#Delete items
@Admin.delete('/delete_items/{id}',status_code=204)
async def delete_items(id : int,payload=protected):
  authorize(payload)
  item_value = session.query(items).filter(items.id == id).first()
  if item_value is None :
    raise  HTTPException(status_code=400,detail='item not found')
  
  else :
   session.delete(item_value)
   session.commit()


#Make user to admin

@Admin.get('/approve',status_code=200)
async def approve(username : str ,payload = protected):
  check_owner(payload)
  user = session.query(users).filter(users.username == username).first()
  if user is None :
    raise HTTPException(status_code=404,detail='User Not Found')
  if not user.admin :
     user.admin = True
     session.commit()
     return {'msg' : 'Approved Successfully'}
  else :
    raise HTTPException(status_code = 400,detail = 'user is already admin')



#make admin to user


@Admin.get('/demote',status_code=200)
async def approve(username : str ,payload = protected):
  check_owner(payload)
  if payload['username'] == username :
    raise HTTPException(status_code=400,detail='you cannot demote yourself')
  user = session.query(users).filter(users.username == username).first()
  if user is None :
    raise HTTPException(status_code=404,detail='User Not Found')
  if  user.admin :
     user.admin = False
     session.commit()
     return {'msg' : 'Demoted Successfully'}
  else :
    raise HTTPException(status_code = 400,detail = 'it is user not admin')

#Get admin list

@Admin.get('/admin_list',status_code=200)
async def admin_list(payload = protected):
  authorize(payload)
  Users_list = session.query(users).filter(users.admin == True).all()
  if Users_list is None :
    raise HTTPException(status_code=404,detail='No admins')
  return Users_list

