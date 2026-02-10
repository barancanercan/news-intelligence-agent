import feedparser
import datetime
from dateutil import parser as date_parser
import time
import sys
import os
from urllib.parse import quote

# Proje kök dizinini sys.path'e ekleyerek 'storage' modülünü import edilebilir hale getir
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.append(_project_root)

from storage.session import get_db_session, engine
from storage.models import NewsArticle, Base

# --- Kategorize Edilmiş Genişletilmiş Sorgu Listesi ---
# Her kategori, ilgili haberleri etiketlemek için kullanılır.
CATEGORIZED_QUERIES = {
    "Ana Kurumlar ve Yönetim": [
        '"TBMM" OR "Türkiye Büyük Millet Meclisi"',
        '"Cumhurbaşkanı" OR "Cumhurbaşkanlığı" OR "RTE" OR "Recep Tayyip Erdoğan"',
        '"Ankara Büyükşehir Belediyesi" OR "ABB"',
        '"İstanbul Büyükşehir Belediyesi" OR "İBB" OR "IBB"',
        '"Belediyesi" OR "Belediye"',
    ],
    "Siyasi Partiler": [
        '"AK Parti" OR "Adalet ve Kalkınma Partisi" OR "AKP"',
        '"CHP" OR "Cumhuriyet Halk Partisi"',
        '"MHP" OR "Milliyetçi Hareket Partisi"',
        '"DEM Parti"',
        '"İYİ Parti"',
        '"Yeniden Refah Partisi" OR "YRP"',
        '"Zafer Partisi"',
    ],
    "Liderler": [
        '"Genel Başkan" OR "belediye başkanı" OR "milletvekili"',
        '"Özgür Özel" OR "Mansur Yavaş" OR "Ekrem İmamoğlu"',
        '"Devlet Bahçeli"',
        '"Tuncer Bakırhan" OR "Tülay Hatimoğulları"',
        '"Müsavat Dervişoğlu"',
        '"Fatih Erbakan"',
    ],
    "Bakanlıklar ve Kilit Roller": [
        '"Dışişleri Bakanlığı"',
        '"Hazine ve Maliye Bakanlığı"',
        '"İçişleri Bakanlığı"',
        '"Milli Savunma Bakanlığı"',
        '"Adalet Bakanlığı"',
        '"Sağlık Bakanlığı"',
    ],
    "Temel Politik ve Ekonomik Gündem": [
        '"enflasyon" OR "faiz kararı" OR "ekonomi"',
        '"seçim" OR "sandık" OR "YSK"',
        '"dış politika"',
        '"terörle mücadele" OR "milli güvenlik"',
        '"yeni yasa" OR "kanun teklifi"',
        '"bakanlar kurulu" OR "kabine toplantısı"',
    ]
}

def initialize_database():
    """Veritabanı ve tabloları oluşturur."""
    print("Veritabanı tabloları oluşturuluyor (eğer mevcut değilse)...")
    Base.metadata.create_all(bind=engine)
    print("Tablolar hazır.")

def fetch_and_filter_news(time_filter_hours: int = 24):
    """
    Kategorize edilmiş sorgu listesindeki her bir sorgu için haberleri çeker,
    zaman filtresi uygular ve kategori etiketiyle birlikte veritabanına kaydeder.
    """
    total_queries = sum(len(queries) for queries in CATEGORIZED_QUERIES.values())
    print(f"{len(CATEGORIZED_QUERIES)} kategori üzerinden toplam {total_queries} sorgu ile haberler çekilecek...")
    
    now = datetime.datetime.now(datetime.timezone.utc)
    time_threshold = now - datetime.timedelta(hours=time_filter_hours)
    
    print(f"Zaman filtresi uygulanıyor: Yalnızca son {time_filter_hours} saatteki haberler işlenecek.")
    print(f"Zaman eşiği (UTC): {time_threshold.strftime('%Y-%m-%d %H:%M:%S')}")

    total_new_articles_count = 0
    processed_urls = set() 

    db_gen = get_db_session()
    db = next(db_gen)
    
    try:
        # Kategoriler ve sorgular üzerinde döngü
        for category, queries in CATEGORIZED_QUERIES.items():
            print(f"\n--- Kategori: {category} ---")
            for query in queries:
                safe_query = quote(query)
                rss_url = f"https://news.google.com/rss/search?q={safe_query}&hl=tr&gl=TR&ceid=TR:tr"
                print(f"  Sorgu: '{query}'")
                
                feed = feedparser.parse(rss_url)
                
                if feed.bozo:
                    print(f"    HATA: RSS beslemesi okunurken bir sorun oluştu: {feed.bozo_exception}")
                    continue

                query_new_articles_count = 0
                for entry in feed.entries:
                    if entry.link in processed_urls:
                        continue

                    published_time_str = entry.get("published")
                    if not published_time_str:
                        continue

                    published_time = date_parser.parse(published_time_str).astimezone(datetime.timezone.utc)

                    if published_time < time_threshold:
                        continue

                    exists = db.query(NewsArticle).filter(NewsArticle.url == entry.link).first()
                    if exists:
                        continue
                    
                    processed_urls.add(entry.link)

                    new_article = NewsArticle(
                        url=entry.link,
                        title=entry.title,
                        category=category,  # <-- KATEGORİ ETİKETİ EKLENDİ
                        published_at=published_time,
                        collected_at=now
                    )
                    db.add(new_article)
                    query_new_articles_count += 1
                
                if query_new_articles_count > 0:
                    total_new_articles_count += query_new_articles_count
                    print(f"    -> Bu sorgudan {query_new_articles_count} yeni haber bulundu.")

        if total_new_articles_count > 0:
            db.commit()
            print(f"\nBaşarılı: Veritabanına toplam {total_new_articles_count} yeni haber eklendi.")
        else:
            print("\nVeritabanına eklenecek yeni haber bulunamadı.")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("--- Kategorize Edilmiş Haber Toplama Betiği Başlatıldı ---")
    start_time = time.time()
    
    # Yeni 'category' kolonu eklendiği için eski veritabanını silmek önemlidir.
    db_path = os.path.join(_project_root, 'news.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Eski veritabanı dosyası (news.db) yeni şema için silindi.")

    initialize_database()
    fetch_and_filter_news(time_filter_hours=24)
    
    end_time = time.time()
    print(f"\nİşlem {end_time - start_time:.2f} saniyede tamamlandı.")
    print("--- Betik Tamamlandı ---")
