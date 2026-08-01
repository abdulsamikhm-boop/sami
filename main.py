from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import RedirectResponse 
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,Session,sessionmaker,Mapped,mapped_column
from pydantic import BaseModel

DATABASE_URL = 'sqlite:///./todo.db'
engine = create_engine(DATABASE_URL,connect_args={'check_same_thread':False})
sessionlocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
base = declarative_base()

class todoitem(base):
    __tablename__ = 'todo'
    id :Mapped[int] =mapped_column(Integer,primary_key=True,index=True)
    title:Mapped[str] =mapped_column(String,index=True)
    description : Mapped[str | None]=mapped_column(String,index=True,default=None)
base.metadata.create_all(bind=engine)

class todocreate(BaseModel):
    title : str
    description : str | None = None
class todoresposne(BaseModel):
    id : int
    title:str
    description : str |  None = None

    class Config:
        from_attributes =True

def get_db():
    db =sessionlocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title='fastapi database app')

@app.get('/',include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.post('/todo/',response_model=todoresposne) 
def create_todo(todo:todocreate,db:Session=Depends(get_db)):
    db_todo = todoitem(title =todo.title,description =todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get('/todo/',response_model=list[todoresposne])
def read_todo(db:Session=Depends(get_db)):
    return db.query(todoitem).all()


@app.delete('/todo/{todo_id}')
def delete_todo(todo_id :int,db:Session=Depends(get_db)):
    db_todo = db.query(todoitem).filter(todoitem.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code = 404, detail='404 page not found')
    db.delete(db_todo)
    db.commit()
    return {'detail':f'deleted item {todo_id}'}
                

