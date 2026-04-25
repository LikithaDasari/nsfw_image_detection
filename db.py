from sqlalchemy import create_engine, Column, Boolean, Float, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base = declarative_base()


class NSFWLog(Base):
    __tablename__ = "nsfw_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), nullable=False)
    timestamp = Column(TIMESTAMP)
    nsfw_detected = Column(Boolean)
    confidence = Column(Float)


Base.metadata.create_all(bind=engine)
