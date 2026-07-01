

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey



from datetime import datetime
from app.core.database import Base





class Analysis(Base):
    __tablename__ = "analysis"

    id           = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    sport    = Column(String, nullable=False)
    discipline    = Column(String, nullable=False)
    input_text    = Column(Text, nullable=False)
    score   = Column(Integer, nullable=False)
    strengths   = Column(Text, nullable=False)
    improvements   = Column(Text, nullable=False)
    recommendations   = Column(Text, nullable=False)
    created_at   = Column(DateTime, default=datetime.utcnow)

    
    

    

    def __repr__(self):
     return  f"<Analysis {self.id} by user {self.user_id}>"
