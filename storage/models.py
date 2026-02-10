from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class NewsArticle(Base):
    """
    Veritabanında haber makalelerini temsil eden SQLAlchemy modeli.
    """
    __tablename__ = 'news_articles'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text) # Haber içeriğinin tam metni (parse işleminden sonra)
    
    # Haberin hangi sorgu kategorisinden geldiğini belirten etiket
    category = Column(String, nullable=False)
    
    # RSS beslemesinden gelen orijinal yayınlanma tarihi
    published_at = Column(DateTime(timezone=True), nullable=False)
    
    # Bizim sistemi kullanarak veriyi topladığımız tarih
    collected_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<NewsArticle(category='{self.category}', title='{self.title[:30]}...')>"

if __name__ == '__main__':
    engine = create_engine('sqlite:///../news.db')
    print("Veritabanı modeli tanımlandı. Tablo oluşturuluyor...")
    Base.metadata.create_all(engine)
    print("Tablo 'news_articles' başarıyla oluşturuldu veya güncellendi.")
