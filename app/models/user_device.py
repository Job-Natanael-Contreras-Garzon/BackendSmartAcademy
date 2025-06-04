from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class UserDevice(Base):
    __tablename__ = "user_devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_token = Column(String, unique=True, index=True, nullable=False) # Token del dispositivo (ej. FCM token)
    device_type = Column(String, nullable=True) # ej. "android", "ios", "web"
    last_login = Column(DateTime(timezone=True), server_default=func.now())
    app_version = Column(String, nullable=True)

    user = relationship("User", back_populates="devices")

    def __repr__(self):
        return f"<UserDevice id={self.id} user_id={self.user_id} type={self.device_type}>"
