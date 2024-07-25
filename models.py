from sqlalchemy import Column, String, ForeignKey, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from infra import Base
import cuid

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=cuid.cuid)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Relationships
    sent_messages = relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    received_messages = relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver')
    connections = relationship('Connection', foreign_keys='Connection.user_id', back_populates='user')

class Message(Base):
    __tablename__ = 'messages'

    id = Column(String, primary_key=True, default=cuid.cuid)
    sender_id = Column(String, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(String, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    sender = relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')

class Connection(Base):
    __tablename__ = 'connections'

    id = Column(String, primary_key=True, default=cuid.cuid)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    friend_id = Column(String, ForeignKey('users.id'), nullable=False)

    # Relationships
    user = relationship('User', foreign_keys=[user_id], back_populates='connections')
    friend = relationship('User', foreign_keys=[friend_id])

    # Unique constraint to ensure a unique connection
    __table_args__ = (
        UniqueConstraint('user_id', 'friend_id', name='unique_user_friend_pair'),
    )

