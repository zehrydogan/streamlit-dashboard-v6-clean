import pandas as pd, numpy as np, glob, re, unicodedata
from sqlalchemy import create_engine

pd.set_option("future.no_silent_downcasting", True)

# Yardımcı fonksiyonlar
def temizle_kolon_adlari(df): df.columns = [c.strip() for c in df.columns]; return df

def temizle_sayi(x):
    try:
        x = str(x).replace("₺", "").strip()
        if "," in x and "." in x: x = x.replace(".", "").replace(",", ".")
        else: x = x.replace(",", ".")
        return float(x)
    except Exception: return 0.0

def temizle_musteri(a): return "" if pd.isnull(a) else re.sub(r"\s+", " ", str(a).strip()).title()

def nfkd_lower(s): return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().strip()

def fillna_safely(df):
    dt = df.select_dtypes(include=["datetime64[ns]"]).columns
    df[dt] = df[dt].fillna(pd.NaT)
    df[df.columns.difference(dt)] = df[df.columns.difference(dt)].fillna(0)
    return df

def normalize_str(s):
    if pd.isnull(s): return ""
    s = str(s).lower()
    s = re.sub(r"\s+", "", s)
    s = s.replace("ı", "i").replace("İ", "i").replace("ü", "u").replace("ğ", "g")
    s = s.replace("ş", "s").replace("ö", "o").replace("ç", "c")
    return s.strip()

# MySQL bağlantısı
eng = create_engine("mysql+pymysql://root:Dpb2025++@localhost:3306/satisdb")

# 1. Excel Dosyalarını Oku
sip_files = glob.glob("Siparisler*.xlsx")
if not sip_files:
    raise FileNotFoundError("Siparisler*.xlsx yok!")

tum = pd.concat([pd.read_excel(f) for f in sip_files], ignore_index=True)
iade_df = pd.read_excel("İadeler.xlsx")
toptan_df = pd.read_excel("Toptan.xlsx")
maliyet_df = pd.read_excel("Maliyet.xlsx")
hali_maliyet_df = pd.read_excel("All.xlsx", engine="openpyxl")
# ---------------------------
# ÜRÜNLER EXCELİ: 'urunler.xlsx'
# ---------------------------
urunler_df = pd.read_excel("urunler.xlsx", engine="openpyxl")
temizle_kolon_adlari(urunler_df)

# Kolon isimlerini normalize et
urunler_df.rename(columns={
    "Stok Kodu": "stok_kodu",
    "Ürün Adı": "urun_adi",
    "Stok": "stok",
    "Ana Ürün Kodu": "ana_urun_kodu",
    "Maliyet Fiyatı (KDV Dahil)": "maliyet_kdv_dahil",
    "Para Birimi": "para_birimi",
    "KDV Oranı": "kdv_orani",
}, inplace=True)

# Stok sütununu temizle
# Stok sütununu güvenle sayıya çevir (boşlukları ve metinleri temizleyerek)
urunler_df["stok"] = urunler_df["stok"].astype(str).str.replace(",", ".").str.strip()
urunler_df["stok"] = pd.to_numeric(urunler_df["stok"], errors="coerce")

# Sadece gerçekten stokta olmayanları al (stok 0 veya negatif olanlar)
stokta_olmayan_df = urunler_df[urunler_df["stok"] <= 0].copy()

# SQL'e kaydet
urunler_df.to_sql("urunler", eng, if_exists="replace", index=False)
stokta_olmayan_df.to_sql("stokta_olmayan", eng, if_exists="replace", index=False)

print(f"🛑 Stokta olmayan ürün sayısı: {len(stokta_olmayan_df)} / {len(urunler_df)} toplam")

for d in (tum, iade_df, toptan_df, maliyet_df, hali_maliyet_df):
    temizle_kolon_adlari(d)

# hali_maliyet kolonlarını sadeleştir
hali_maliyet_df.rename(columns={
    "Magaza": "magaza",
    "Pazaryeri": "pazaryeri",
    "Tedarikçi Stok Kodu": "tedarikci_stok_kodu",
    "Maliyet": "maliyet"
}, inplace=True)

# Sayısal temizlik
for c in ["Satır Fiyat", "Satır Komisyon", "Ürün Toplam Maliyet"]:
    tum[c] = tum[c].apply(temizle_sayi)
iade_df["Satır Fiyat"] = iade_df["Satır Fiyat"].apply(temizle_sayi)

# Müşteri adı temizliği
tum["Fatura - Müşteri"] = tum["Fatura - Müşteri"].astype(str).apply(temizle_musteri)
iade_df["Fatura - Müşteri"] = iade_df["Fatura - Müşteri"].astype(str).apply(temizle_musteri)

# Kargo sabit 0
tum["kargo_fiyat"] = 0.0

# Kar hesapla
tum.drop_duplicates(inplace=True)
tum["Kar"] = tum["Satır Fiyat"] - tum["Satır Komisyon"] - tum["Ürün Toplam Maliyet"]

# İade eşleşme ve kar sıfırla
key = lambda df: df["Sipariş No"].astype(str) + "|" + df["Stok Kodu"].astype(str)
tum["key"] = key(tum); iade_df["key"] = key(iade_df)
tum.loc[tum["key"].isin(iade_df["key"]), "Kar"] = 0.0

# iptal / aktif durumu
durum = tum.get("Sipariş Satır Durumu", "").map(nfkd_lower)
iptal = durum.str.contains("iptal") | durum.str.contains("cancel")
tum["siparis_durumu"] = np.where(iptal, "iptal", "aktif")
tum.loc[iptal, "Kar"] = 0.0
iptal_df = tum[iptal].copy()

# Sipariş tarihi
tum["siparis_tarihi"] = pd.to_datetime(tum["Sip. Tarihi"], errors="coerce", dayfirst=True).dt.date

# Toptan maliyet
maliyet_map = dict(zip(maliyet_df["Stok Kodu"], maliyet_df["Maliyet Fiyatı"].apply(temizle_sayi)))
toptan_df["maliyet_fiyati"] = toptan_df["Stok Kodu"].map(maliyet_map).apply(temizle_sayi)
toptan_df["Miktar"] = pd.to_numeric(toptan_df["Miktar"], errors="coerce") if "Miktar" in toptan_df.columns else 0
toptan_df["toplam_maliyet"] = toptan_df["Miktar"] * toptan_df["maliyet_fiyati"]
toptan_df["kar"] = toptan_df["Tutarı (KDV Dahil)"].apply(temizle_sayi) - toptan_df["toplam_maliyet"]
toptan_df["siparis_tarihi"] = pd.to_datetime(toptan_df["Tarihi"].astype(str) + " " + toptan_df["Saati"].astype(str), errors="coerce").dt.date

# siparis_kar dataframe
# siparis_kar dataframe
kolonlar = [
    "Pazaryeri", "Sipariş No", "Stok Kodu", "Fatura - Müşteri", "Ürün",
    "Satır Fiyat", "Satır Komisyon", "Ürün Toplam Maliyet", "Kar",
    "siparis_tarihi", "siparis_durumu", "kargo_fiyat", "Fatura - İl", "Fatura - İlçe"  #
]

if "Mağaza" in tum.columns:
    kolonlar.insert(1, "Mağaza")

siparis_kar_df = tum[kolonlar].copy()

# Kolon isimlerini normalize et
yeni_kolonlar = [
    "pazaryeri", "magaza", "siparis_no", "stok_kodu", "musteri_adi", "urun_adi",
    "satir_fiyat", "satir_komisyon", "urun_toplam_maliyet", "kar",
    "siparis_tarihi", "siparis_durumu", "kargo_fiyat", "sevk_il", "sevk_ilce"
]

siparis_kar_df.columns = yeni_kolonlar


# NULL temizle
for d in (iptal_df, siparis_kar_df, iade_df, toptan_df, maliyet_df, hali_maliyet_df):
    fillna_safely(d)

#Maliyeti 0 olan siparişleri al
mask = siparis_kar_df["urun_toplam_maliyet"] == 0
maliyetsiz = siparis_kar_df[mask].copy()

#Hali maliyet tablosunda aynı stok kodundan birden fazla varsa sonuncusunu al
hali_maliyet_df = hali_maliyet_df.drop_duplicates(
    subset=["tedarikci_stok_kodu"],
    keep="last"
)

# Eşleştir → sadece birebir (case-sensitive) stok kodu ile
merged = maliyetsiz.merge(
    hali_maliyet_df[["tedarikci_stok_kodu", "maliyet"]],
    left_on="stok_kodu",
    right_on="tedarikci_stok_kodu",
    how="left"
)

# Eşleşmeyenleri göster
eslesmeyenler = merged[merged["maliyet"].isna()]
if not eslesmeyenler.empty:
    print(f"🚨 Eşleşmeyen kayıt sayısı: {len(eslesmeyenler)}")
    print(eslesmeyenler[["stok_kodu"]].drop_duplicates().head())

# ✅ Eşleşenleri güncelle
guncellenecek_indexler = siparis_kar_df[mask].index
yeni_maliyetler = merged["maliyet"].fillna(0).apply(temizle_sayi).values

if len(guncellenecek_indexler) == len(yeni_maliyetler):
    siparis_kar_df.loc[guncellenecek_indexler, "urun_toplam_maliyet"] = yeni_maliyetler
    print("✅ Maliyet güncellemesi başarılı.")
else:
    print("❌ UYARI: Uzunluk uyuşmazlığı! Güncelleme yapılmadı.")
    print(f"mask: {len(guncellenecek_indexler)}, gelen: {len(yeni_maliyetler)}")

# 🧮 Karı yeniden hesapla
siparis_kar_df["kar"] = (
    siparis_kar_df["satir_fiyat"]
    - siparis_kar_df["satir_komisyon"]
    - siparis_kar_df["urun_toplam_maliyet"]
)
# -------------------------------------------------------
# 🔄 KARGO ve PaymentDiscount satırlarını kara ekle
# -------------------------------------------------------

# 1. KARGO ve PaymentDiscount satırlarını ayır
ek_kalemler = siparis_kar_df[
    siparis_kar_df["stok_kodu"].str.upper().isin(["KARGO", "PAYMENTDISCOUNT"])
]

# 2. Gerçek ürünleri filtrele
urunler = siparis_kar_df[
    ~siparis_kar_df["stok_kodu"].str.upper().isin(["KARGO", "PAYMENTDISCOUNT"])
].copy()

# 3. Ek kalemlerin siparis_no bazında toplam satır fiyatı
ek_tutar_df = (
    ek_kalemler.groupby("siparis_no")["satir_fiyat"]
    .sum()
    .reset_index()
    .rename(columns={"satir_fiyat": "ek_kalem_tutari"})
)

# 4. Ürünlerle birleştir
urunler = urunler.merge(ek_tutar_df, on="siparis_no", how="left")
urunler["ek_kalem_tutari"] = urunler["ek_kalem_tutari"].fillna(0)

# 5. Karı yeniden güncelle: mevcut kar + ek kalem fiyatı
urunler["kar"] = urunler["kar"] + urunler["ek_kalem_tutari"]

# 6. siparis_kar_df'i sadece ürünlerle yeniden oluştur
siparis_kar_df = urunler

# 5. MySQL'e yaz
eng = create_engine("mysql+pymysql://root:Dpb2025++@localhost:3306/satisdb")
siparis_kar_df.to_sql("siparis_kar", eng, if_exists="replace", index=False)
iptal_df.to_sql("iptal_siparisler", eng, if_exists="replace", index=False)
iade_df.to_sql("iadeler", eng, if_exists="replace", index=False)
toptan_df.to_sql("toptan_kar", eng, if_exists="replace", index=False)
maliyet_df.to_sql("maliyet", eng, if_exists="replace", index=False)
hali_maliyet_df.to_sql("hali_maliyet", eng, if_exists="replace", index=False)

# 📊 Eşleşme İstatistikleri
toplam_maliyet_0 = len(maliyetsiz)
eslesen_sayisi = toplam_maliyet_0 - len(eslesmeyenler)
eslesmeyen_sayisi = len(eslesmeyenler)

print(f"\n📊 Eşleşme özeti:")
print(f"✅ Eşleşen kayıt sayısı   : {eslesen_sayisi}")
print(f"❌ Eşleşmeyen kayıt sayısı: {eslesmeyen_sayisi}")
print(f"🔢 Toplam işlenen kayıt    : {toplam_maliyet_0}")

print("🎯 Tüm veriler başarıyla işlendi ve MySQL'e aktarıldı.")

# hali_maliyet'te olmayan stok_kodlarını tespit et
maliyetli_kodlar = set(hali_maliyet_df["tedarikci_stok_kodu"].astype(str))
maliyetsiz_kodlar = set(siparis_kar_df[siparis_kar_df["urun_toplam_maliyet"] == 0]["stok_kodu"].astype(str))

eslesmeyen_kodlar = sorted(maliyetsiz_kodlar - maliyetli_kodlar)

# Sonuçları yazdır
print("\n📛 All.xlsx dosyasında olmayan stok_kodları:")
for kod in eslesmeyen_kodlar:
    print("•", kod)

print(f"🔢 Toplam eşleşmeyen stok kodu sayısı: {len(eslesmeyen_kodlar)}")

