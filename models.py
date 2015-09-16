from peewee import *

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
    created_date = DateField()
    
    class Meta:
        order_by = ('header',)

