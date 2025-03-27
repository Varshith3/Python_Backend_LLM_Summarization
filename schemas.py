from pydantic import BaseModel

class MessageCreate(BaseModel):
    conversation_id: int
    content: str

class ConversationCreate(BaseModel):
    name: str

class MessageOut(MessageCreate):
    id: int
    class Config:
        orm_mode = True

class ConversationOut(ConversationCreate):
    id: int
    class Config:
        orm_mode = True
