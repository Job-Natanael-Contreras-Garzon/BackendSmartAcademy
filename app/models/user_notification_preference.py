from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserNotificationPreference(Base):
    __tablename__ = "user_notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False) # unique=True para asegurar una pref por usuario

    # Preferencias específicas (ejemplos)
    email_notifications_enabled = Column(Boolean, default=True)
    push_notifications_enabled = Column(Boolean, default=True)
    new_grade_notifications = Column(Boolean, default=True)
    event_reminders = Column(Boolean, default=True)
    # Añadir más preferencias según sea necesario

    user = relationship("User", back_populates="notification_preferences")

    def __repr__(self):
        return f"<UserNotificationPreference user_id={self.user_id}>"
