from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)

    #def __repr__(self):
    #    return f"<Movie(title={self.title}, year={self.year}, description={self.description}, rating={self.rating})>"