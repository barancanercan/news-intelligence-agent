import sys
import os
from datetime import datetime

# Proje kök dizinini sys.path'e ekle
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.append(_project_root)

from storage.session import get_db_session
from storage.models import NewsArticle

def check_database_content():
    """
    Veritabanındaki haberleri okur ve yayınlanma tarihlerini listeler.
    Bu, zaman filtresinin doğru çalışıp çalışmadığını doğrulamak için kullanılır.
    """
    print("--- Veritabanı İçerik Kontrol Betiği ---")
    
    db_path = os.path.join(_project_root, 'news.db')
    if not os.path.exists(db_path):
        print(f"HATA: Veritabanı dosyası bulunamadı: {db_path}")
        print("Lütfen önce 'collector/fetch.py' betiğini çalıştırdığınızdan emin olun.")
        return

    db_gen = get_db_session()
    db = next(db_gen)
    
    try:
        articles = db.query(NewsArticle).order_by(NewsArticle.published_at.desc()).all()
        
        if not articles:
            print("Veritabanında hiç haber bulunamadı.")
            return
            
        print(f"Veritabanında toplam {len(articles)} haber bulundu.")
        print("Haberler en yeniden eskiye doğru listeleniyor:\n")
        
        now = datetime.now(articles[0].published_at.tzinfo) # Zaman dilimini ilk kayıttan al
        
        for article in articles:
            published_time = article.published_at
            time_diff = now - published_time
            hours_ago = time_diff.total_seconds() / 3600
            
            print(f"- Başlık: {article.title}")
            print(f"  URL: {article.url}")
            print(f"  Yayınlanma Zamanı: {published_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            print(f"  (Yaklaşık {hours_ago:.1f} saat önce)")
            print("-" * 20)
            
    except Exception as e:
        print(f"Veritabanı okunurken bir hata oluştu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_database_content()
