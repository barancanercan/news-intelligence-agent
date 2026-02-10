import sys
import os
import csv
from datetime import datetime

# Proje kök dizinini sys.path'e ekle
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.append(_project_root)

from storage.session import get_db_session
from storage.models import NewsArticle

def export_data_to_csv():
    """
    Veritabanındaki haberleri okur, tarihe göre sıralar ve kategori bilgisiyle
    birlikte bir CSV dosyasına yazar.
    """
    print("--- Veritabanı -> CSV Aktarım Betiği ---")
    
    db_path = os.path.join(_project_root, 'news.db')
    if not os.path.exists(db_path):
        print(f"HATA: Veritabanı dosyası bulunamadı: {db_path}")
        print("Lütfen önce 'collector/fetch.py' betiğini çalıştırdığınızdan emin olun.")
        return

    csv_file_path = os.path.join(_project_root, 'news_report_categorized.csv')
    
    db_gen = get_db_session()
    db = next(db_gen)
    
    try:
        # Haberleri yayınlanma tarihine göre eskiden yeniye sırala
        articles = db.query(NewsArticle).order_by(NewsArticle.published_at.asc()).all()
        
        if not articles:
            print("Veritabanında dışa aktarılacak haber bulunamadı.")
            return
            
        print(f"Veritabanında toplam {len(articles)} haber bulundu.")
        
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            # CSV başlıklarına 'category' eklendi
            fieldnames = ['category', 'published_at', 'collected_at', 'title', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for article in articles:
                writer.writerow({
                    'category': article.category,
                    'published_at': article.published_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'collected_at': article.collected_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'title': article.title,
                    'url': article.url
                })
        
        print(f"Başarılı: {len(articles)} haber, '{csv_file_path}' dosyasına kaydedildi.")

    except Exception as e:
        print(f"Veritabanı okunurken veya CSV yazılırken bir hata oluştu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    export_data_to_csv()
