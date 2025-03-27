from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

# SQLite database URL
DATABASE_URL = "sqlite:///./test.db"  # SQLite is stored in a local file called 'test.db'

# Create the engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # SQLite requires this argument

# Create the base class
Base = declarative_base()

# Create the SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Example Model: Conversation and Message
class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer)
    content = Column(String)
