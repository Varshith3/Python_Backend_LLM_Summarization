import cohere
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base, Conversation, Message
from schemas import MessageCreate, ConversationCreate, MessageOut, ConversationOut
import os
from dotenv import load_dotenv


load_dotenv()   
# Initialize Cohere API client
api_key = os.getenv("COHERE_API_KEY")
cohere_client = cohere.ClientV2(api_key)  

# FastAPI app initialization
app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def summarize_text(text: str):
    try:
        message = f"Generate a concise summary of this text:\n{text}"

        response = cohere_client.chat(
            model="command-a-03-2025",
            messages=[{"role": "user", "content": message}],
        )

        summary = response.message.content[0].text.strip()
        return summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        raise HTTPException(status_code=500, detail="Error during summarization.")


# Existing routes for creating conversations and messages (same as before)
@app.post("/conversations/", response_model=ConversationOut)
def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    db_conversation = Conversation(name=conversation.name)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@app.get("/conversations/", response_model=list[ConversationOut])
def get_conversations(db: Session = Depends(get_db)):
    return db.query(Conversation).all()

@app.post("/messages/", response_model=MessageOut)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = Message(conversation_id=message.conversation_id, content=message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/messages/{conversation_id}", response_model=list[MessageOut])
def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.conversation_id == conversation_id).all()

# New route for summarizing a conversation's messages
@app.get("/summarize/{conversation_id}", response_model=str)
def summarize_conversation(conversation_id: int, db: Session = Depends(get_db)):
    # Get all messages for the specified conversation
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this conversation.")
    
    # Concatenate all message contents into a single string
    text_to_summarize = " ".join([msg.content for msg in messages])

    # Summarize using Cohere
    summary = summarize_text(text_to_summarize)
    return summary
