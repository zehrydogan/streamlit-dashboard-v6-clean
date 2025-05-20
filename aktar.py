import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

excel_dosyasi = "Siparişler.xlsx"

try:
    print("Excel dosyası okunuyor...")
    df = pd.read_excel(excel_dosyasi)
    df.columns = df.columns.str.strip()

    print("Veritabanına bağlanılıyor (ilk bağlantı)...")
    init_engine = create_engine("mysql+pymysql://root:Dpb2025++@localhost:3306")
    with init_engine.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS satisdb"))

    print("satisdb veritabanına bağlanılıyor...")
    engine = create_engine("mysql+pymysql://root:Dpb2025++@localhost:3306/satisdb")

    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS siparisler"))

    print("Veri aktarılıyor...")
    df.to_sql(name="siparisler", con=engine, if_exists="replace", index=False)

    print("Veri başarıyla MySQL veritabanına aktarıldı.")

except FileNotFoundError:
    print("HATA: Excel dosyası bulunamadı.")
except SQLAlchemyError as e:
    print(f"Veritabanı hatası: {e}")
except Exception as e:
    print(f"Beklenmeyen hata: {e}")
