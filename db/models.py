from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from db.database import Base
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    conversations = relationship("Conversation", back_populates="user")
    appointments = relationship("Appointment", back_populates="user")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
    attachments = relationship("Attachment", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True)
    conversation_id = Column(
        String,
        ForeignKey("conversations.id"),
        nullable=False,
        index=True,
    )
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")
    embedding = relationship("Embedding", back_populates="message", uselist=False)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    appointment_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="appointments")


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(String, primary_key=True)
    conversation_id = Column(
        String,
        ForeignKey("conversations.id"),
        nullable=False,
        index=True,
    )
    file_name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    file_type = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    conversation = relationship("Conversation", back_populates="attachments")


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(String, primary_key=True)
    message_id = Column(
        "messages_id",
        String,
        ForeignKey("messages.id"),
        nullable=False,
        index=True,
    )
    embedding_vector = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    message = relationship("Message", back_populates="embedding")


# Backward-compatible aliases for the original class names.
Messages = Message
appointments = Appointment
attachments = Attachment
embeddings = Embedding
