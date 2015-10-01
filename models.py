from peewee import *
import time
from datetime import date

db = SqliteDatabase('blog.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField()
    password = CharField()
    
    class Meta:
        order_by = ('name',)
        
class Post(BaseModel):
    header = CharField()
    text = TextField()
    date = DateField()
    category = CharField()
    
    class Meta:
        order_by = ('date',)
