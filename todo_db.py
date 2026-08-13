from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session, sessionmaker,Mapped, mapped_column
from pydantic import BaseModel

DATABSE_URL = 'sqlite:///.todos.db'

engine = create_engine(DATABSE_URL,connect_args={'check_same_thread':False})
sessionlocal = sessionmaker(autoflush=False, autocommit=False,bind=engine)
base = declarative_base()

class todoitems(base):
    __tablename__ = 'todo'
    id:Mapped[int] = mapped_column(Integer,primary_key=True,index=False)
    title : Mapped[str] = mapped_column(String,index=True)
    description : Mapped [str | None] = mapped_column(String,index=True, default=None)

base.metadata.create_all(bind=engine)

class todoresponse(BaseModel):
    title:str
    description : str | None = None

class todocreate(BaseModel):
    id : int
    title : str
    description : str | None = None

    class Config:
        form_attributes = True
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title='fastapi app')

@app.get('/',include_in_schema=False)
def root():
    return RedirectResponse(url='/docs')

@app.post('/todo/',response_model=todoresponse)
def todo_create(todo: todocreate,db:Session = Depends(get_db)):
    db_todo = todoitems(title = todo.title, description = todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get('/todo/',response_model=list[todoresponse])
def todo_read(db:Session = Depends(get_db)):
    return db.query(todoitems).all()

@app.delete('/todo/{todo_id}')
def todo_delete(todo_id: int,db:Session = Depends(get_db)):
    db_todo = db.query(todoitems).filter(id.todoitems == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404,detail='product not found')
    db.delete(db_todo)
    db.commit()
    return {'details':f'deleted item is {todo_id}'}
