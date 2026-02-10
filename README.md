# News Intelligence Agent

[![Project Status: Active](https://img.shields.io/badge/status-active-success.svg)](https://github.com/barancanercan/news-intelligence-agent)

Sürekli ve otonom bir şekilde politik haberleri toplayan, işleyen ve talep üzerine yapılandırılmış istihbarat raporları sunan bir veri toplama ve işleme sistemi.

## Projeye Genel Bakış

`news-intelligence-agent`, bir sohbet robotu veya anlık analist değildir. Arka planda çalışan, belirlenen zaman aralıklarında web'deki politik haberleri toplayan, veriyi tekilleştirerek depolayan ve yalnızca bir insan tarafından talep edildiğinde analiz edilebilir çıktılar üreten bir **veri toplama sistemidir**.

Sistem, yorumlama, doğrulama veya fikir beyan etme yerine, ham verinin kapsamlı ve sinyal odaklı bir şekilde toplanmasına öncelik verir.

## Temel Özellikler

- **Geniş Kapsamlı Veri Toplama:** Onlarca farklı ve spesifik anahtar kelime (partiler, liderler, kurumlar vb.) üzerinden Google News RSS beslemelerini tarar.
- **Otomatik Kategorizasyon:** Her haberi, hangi arama sorgusu kategorisinden (örn: "Siyasi Partiler", "Ana Kurumlar ve Yönetim") geldiğine göre otomatik olarak etiketler. Bu, verinin daha sonra kolayca filtrelenmesini ve analiz edilmesini sağlar.
- **Zaman Filtreleme:** Yalnızca belirlenen zaman aralığındaki (örn. "son 24 saat") haberleri işleme alır.
- **Veri Tekilleştirme:** Aynı haberin farklı arama sorgularından tekrar gelmesini engelleyerek veritabanı bütünlüğünü korur.
- **Yapısal Depolama:** Toplanan ham haberleri (başlık, URL, kategori, yayınlanma tarihi) SQLite veritabanında, SQLAlchemy ORM aracılığıyla yapısal bir formatta saklar.
- **Kolay Kurulum ve Kullanım:** `requirements.txt` ile bağımlılık yönetimi ve basit Python betikleri ile kolayca çalıştırılabilir.
- **Esnek Yapılandırma:** `collector/fetch.py` içerisindeki `CATEGORIZED_QUERIES` sözlüğü, toplanacak haberlerin konularını ve kategorilerini kolayca özelleştirme imkanı sunar.

## Mimarisi ve Çalışma Prensibi

Sistem, basit ve modüler bir boru hattı (pipeline) mimarisi üzerine kurulmuştur:

1.  **`Collector` (Toplayıcı - `collector/fetch.py`)**
    -   Önceden tanımlanmış ve kategorilere ayrılmış sorgu listesindeki her bir anahtar kelime için Google News RSS beslemelerine istek atar.
    -   Gelen haberleri `published_at` (yayınlanma tarihi) bilgisine göre filtreler.
    -   Daha önce işlenmemiş yeni haberleri, geldiği sorgunun **kategorisiyle etiketleyerek** bir sonraki aşamaya aktarır.

2.  **`Storage` (Depolama - `storage/`)**
    -   `models.py`: `NewsArticle` adlı SQLAlchemy modelini tanımlar. Bu model, haberin kategorisini saklamak için bir `category` kolonu içerir.
    -   `session.py`: Proje ana dizininde `news.db` adlı bir SQLite veritabanı dosyası oluşturur ve veritabanı oturumlarını yönetir.
    -   Toplayıcıdan gelen filtrelenmiş ve etiketlenmiş haberler, bu katman aracılığıyla veritabanına kaydedilir.

3.  **`Scripts` (Yardımcı Betikler - `scripts/`)**
    -   `export_to_csv.py`: Veritabanındaki tüm veriyi, kategori bilgisiyle birlikte analiz ve inceleme için `news_report_categorized.csv` dosyasına aktarır.

## Kurulum ve Başlangıç

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### 1. Projeyi Klonlayın

```bash
git clone https://github.com/barancanercan/news-intelligence-agent.git
cd news-intelligence-agent
```

### 2. Sanal Ortam (Virtual Environment) Oluşturun (Önerilir)

```bash
# Sanal ortamı oluştur
python3 -m venv .venv

# Sanal ortamı aktif et (Linux/macOS)
source .venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

## Kullanım

Kurulum tamamlandıktan sonra, aşağıdaki betikleri çalıştırarak sistemi kullanabilirsiniz.

### 1. Haberleri Toplama ve Kategorize Etme

Aşağıdaki komut, `collector/fetch.py` betiğini çalıştırır. Bu betik, yapılandırılmış sorgu listesini kullanarak son 24 saatteki haberleri toplar, kategorize eder ve `news.db` veritabanına kaydeder.

*Not: Betik, her çalıştırmada eski `news.db` dosyasını otomatik olarak silerek temiz bir başlangıç yapar.*

```bash
python collector/fetch.py
```

### 2. Veriyi İnceleme (CSV Olarak)

Toplanan ve kategorize edilen verileri daha kolay incelemek için aşağıdaki komutu çalıştırın. Bu komut, veritabanındaki tüm haberleri `news_report_categorized.csv` adlı bir dosyaya aktarır.

```bash
python scripts/export_to_csv.py
```
Oluşturulan `news_report_categorized.csv` dosyasını bir e-tablo programı ile açtığınızda, her haberin başında bir `category` sütunu göreceksiniz.

## Yapılandırma (Konfigürasyon)

Haber toplama işleminin kapsamını ve kategorilerini değiştirmek çok kolaydır. `collector/fetch.py` dosyasını açın ve `CATEGORIZED_QUERIES` sözlüğünü kendi ihtiyaçlarınıza göre düzenleyin. Yeni kategoriler veya anahtar kelimeler ekleyerek sistemin daha farklı alanlardan haber toplamasını sağlayabilirsiniz.

## Proje Durumu

Bu proje aktif olarak geliştirilmektedir. Mevcut odak, veri toplama (`collector`) ve depolama (`storage`) katmanlarının sağlamlaştırılmasıdır. Gelecek adımlar arasında ham metin ayrıştırma (`parser`), haber önem sıralaması (`ranker`) ve özet raporlama (`reporting`) modüllerinin geliştirilmesi bulunmaktadır.
