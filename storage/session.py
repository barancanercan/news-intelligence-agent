from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Projenin kök dizinini bul
# Bu dosyanın bulunduğu yer: /path/to/project/storage/session.py
# Kök dizin: /path/to/project/
# Bu, betiğin nereden çalıştırıldığına bakılmaksızın veritabanı yolunun doğru olmasını sağlar.
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(_project_root, 'news.db')}"

# create_engine, veritabanı ile ilk bağlantı noktasını oluşturur.
# connect_args, SQLite'ın thread güvenliği için gereklidir.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# sessionmaker, veritabanı ile yapılacak tüm konuşmalar için bir 'fabrika' oluşturur.
# Bu fabrika, her işlem için yeni bir Session nesnesi üretir.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """
    Bir veritabanı oturumu (session) oluşturur ve bunu bir 'yield' ile döndürür.
    Bu yapı, oturumun kullanıldıktan sonra düzgün bir şekilde kapatılmasını sağlar.
    
    Kullanım:
    db = get_db_session()
    try:
        # db üzerinde işlemler yap
        ...
    finally:
        db.close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == '__main__':
    # Bu dosya doğrudan çalıştırıldığında, veritabanı bağlantısını test eder.
    print(f"Veritabanı bağlantısı için URL: {DATABASE_URL}")
    try:
        # Bağlantıyı test etmek için bir session açıp kapat
        db_gen = get_db_session()
        db = next(db_gen)
        print("Veritabanı oturumu başarıyla açıldı.")
        db.close()
        print("Veritabanı oturumu başarıyla kapatıldı.")
        print("Bağlantı başarılı!")
    except Exception as e:
        print(f"Veritabanı bağlantısı başarısız: {e}")
