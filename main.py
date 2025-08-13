from enum import IntEnum
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

api = FastAPI()


class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

# ...代表必填欄位, description : 欄位說明
class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description='Name of the todo')
    todo_description: str = Field(..., description='Description of the todo')
    priority: Priority = Field(default=Priority.LOW, description='Priority of the todo')

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description='Unique identifier of the todo')

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description='Name of the todo')
    todo_description: Optional[str] = Field(None, description='Description of the todo')
    priority: Optional[Priority]= Field(None, description='Priority of the todo')





all_todos = [
    Todo(todo_id = 1, todo_name='Clean house', todo_description = 'Clean the house', priority=Priority.HIGH),
    Todo(todo_id = 2, todo_name='Read', todo_description = 'Read 10 pages', priority=Priority.MEDIUM),
    Todo(todo_id = 3, todo_name='Shop', todo_description = 'Go shopping', priority=Priority.LOW),
    Todo(todo_id = 4, todo_name='Study', todo_description = 'Study for exam', priority=Priority.MEDIUM),
    Todo(todo_id = 5, todo_name='Meditate', todo_description = 'Meditate 20 minutes', priority=Priority.LOW)
]

#GET, POST, PUT, DELETE
@api.get('/')
def read_root():
    return {"message": "Hello FastAPI!"}

@api.get('/todos/{todo_id}', response_model=Todo)
def get_todo(todo_id:int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail='Todo not found')
        
# int 2, str '2'
@api.get('/todos', response_model=List[Todo])
def get_todos(first_n:int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos
    
@api.post('/todos', response_model=Todo)
def create_todo(todo:TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1
    new_todo = Todo(todo_id = new_todo_id, 
                    todo_name=todo.todo_name, 
                    todo_description=todo.todo_description,
                    priority=todo.priority)
    all_todos.append(new_todo)
    return new_todo

@api.put('/todos/{todo_id}', response_model=Todo)
def update_todo(todo_id:int, updated_todo:TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            if updated_todo.todo_name is not None:
                todo.todo_name= updated_todo.todo_name
            if updated_todo.description is not None:
                todo.todo_description= updated_todo.todo_description
            if updated_todo.priority is not None:
                todo.priority = updated_todo.priority
            return todo
    raise HTTPException(status_code=404, detail='Todo not found')

@api.delete('/todos/{todo_id}', response_model=Todo)
def delete_todo(todo_id:int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            delete_todo = all_todos.pop(index)
            return delete_todo
    raise HTTPException(status_code=404, detail='Todo not found')