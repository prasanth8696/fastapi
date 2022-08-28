from enum import Enum
from pydantic import BaseModel,Field

class SignUpModel(BaseModel):
   username : str
   email : str
   password : str

   class Config :
     orm_mode = True
     example = {
        'example' : {
      'username' : 'Shan',
      'email'    :  'ayyappand464@gmail.com',
       'password' : '12345'

             }

           }

class LoginModel(BaseModel):
   username :str
   password : str


class OrderModel(BaseModel) :
  payment_method = str
  address = str
  class Config :
    orm_mode = True
    schema_extra = {

            'example' : {
                  'payment_method' : 'Cash on delivery',
                  'address' : 'chennai'}
              }

class ItemModel(BaseModel):
  name : str
  price : int
  discount : int = Field(default=0,ge=0,le=90)
  quantity = int
  class Config :
    orm_mode = True


class UpdateModel(BaseModel) :
  id : int
  discount : int = Field(default=0,ge=0,le=100)
  quantity : int = Field(default=10)
  class Config :
     orm_mode = True
