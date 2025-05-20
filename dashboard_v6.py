import streamlit as st
import pandas as pd
import datetime
import altair as alt
import unicodedata
import json
import geopandas as gpd
import plotly.express as px

st.set_page_config(page_title="Satış Dashboard", layout="wide")

st.markdown("""
<style>
/* Sidebar arka planı ve genel yazı rengi */
section[data-testid="stSidebar"] {
    background-color: #1e1e1e !important;
    color: white;
}
.st-emotion-cache-p7i6r9 {
    font-family: "Source Sans Pro", sans-serif;
    font-size: 1rem;
    color: rgb(247 247 247);
}
/* Sidebar başlık ve metinler */
section[data-testid="stSidebar"] .css-1v0mbdj,
section[data-testid="stSidebar"] .css-10trblm,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #f0f0f0 !important;
}

/* Input alanlarını koyulaştır (selectbox, input vs) */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] select,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] .stMultiSelect,
section[data-testid="stSidebar"] .stDateInput,
section[data-testid="stSidebar"] .stTextInput,
section[data-testid="stSidebar"] .stSelectbox {
    background-color: #2c2c2c !important;
    color: white !important;
    border: 1px solid #444 !important;
    border-radius: 5px;
}

/* Radio buton metinlerini beyaz ve görünür yap */
div[data-baseweb="radio"] label > div:first-child > span {
    color: white !important;
    opacity: 1 !important;
    font-weight: 500;
}

/* Seçili radio dış kutusu beyaz */
div[data-baseweb="radio"] input[type="radio"]:checked + div {
    background-color: white !important;
    border-color: white !important;
}

/* Seçili radio iç daireyi siyah yap */
div[data-baseweb="radio"] input[type="radio"]:checked + div::before {
    background-color: black !important;
}
</style>
""", unsafe_allow_html=True)



# --------------------
# GÖMÜLÜ CSS
# --------------------
st.markdown("""
<style>
body { background-color: #f5f6fa; }
header[data-testid="stHeader"] { margin-top: -5%; }
.block-container {
    padding-top: 0.0rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
[data-testid="metric-container"] {
    background-color: white;
    padding: 20px 15px;
    border: 1px solid #dcdde1;
    border-radius: 12px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
    margin: 5px;
    text-align: center;
}
[data-testid="metric-container"] > div > div > span {
    font-size: 24px;
    font-weight: 600;
    color: #2f3640;
}
[data-testid="metric-container"] > label {
    font-size: 14px;
    color: #718093;
}
</style>
""", unsafe_allow_html=True)

# -------------------- MAĞAZA NORMALİZASYONU --------------------
def normalize_magaza(s):
    if pd.isnull(s):
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = s.encode("ASCII", "ignore").decode("utf-8").lower().strip()
    s = s.replace(" ", "")
    if "ilyaki" in s:
        return "ilyaki"
    elif "depoba" in s:
        return "depoba"
    elif "latte" in s:
        return "latte"
    elif "sporsuit" in s:
        return "sporsuit"
    elif "aydahome" in s or "ayda" in s:
        return "aida home"
    elif "perakende" in s:
        return "perakende"
    else:
        return s


df = pd.read_excel("Siparisler.xlsx")
df["siparis_tarihi"] = pd.to_datetime(df["Sip. Tarihi"], errors="coerce")
df.columns = [c.strip() for c in df.columns]  # boşlukları temizle
df.rename(columns={"Mağaza": "magaza"}, inplace=True)  # Türkçe karakteri düzelt


toptan_df = pd.read_excel("Toptan.xlsx")
toptan_df.columns = [c.strip() for c in toptan_df.columns]  # Tüm sütun adlarını temizle

# Kontrollü birleştir
tarih = toptan_df["Tarihi"].astype(str).str.strip()
saat = toptan_df["Saati"].astype(str).str.strip()

toptan_df["siparis_tarihi"] = pd.to_datetime(tarih + " " + saat, errors="coerce")



toptan_df = toptan_df.rename(columns={
    "Pazaryeri": "pazaryeri",
    "Stok Kodu": "stok_kodu",
    "Tutarı (KDV Dahil)": "satir_fiyat",
    "maliyet_fiyati": "urun_toplam_maliyet",
    "kar": "kar"
})
print(df.columns)

toptan_df["satir_komisyon"] = 0
toptan_df["kargo_fiyat"] = 0
toptan_df["siparis_durumu"] = "aktif"
toptan_df["magaza"] = "perakende"
toptan_df["siparis_no"] = "TP" + toptan_df.index.astype(str)
toptan_df["musteri_adi"] = "-"
toptan_df["urun_adi"] = "-"
geo_path = "turkiye_il_sinirlar.json"  # ← kendi dosya adın neyse o
with open(geo_path, "r", encoding="utf-8") as f:
    turkiye_geojson = json.load(f)

# Eksik kolonları df'e uygun ekle
for col in df.columns:
    if col not in toptan_df.columns:
        toptan_df[col] = 0

# Sıralamayı df ile eşle
toptan_df = toptan_df[df.columns]
# Manuel veri
# -------------------- MANUEL VERİ EKLE (SPORSUIT - PERAKENDE) --------------------
manuel_veri = pd.DataFrame([{
    "siparis_no": "TP_MANUEL",
    "siparis_tarihi": pd.to_datetime("2025-05-15"),
    "stok_kodu": "SPRS-TEST-001",
    "satir_fiyat": 3200.0,
    "urun_toplam_maliyet": 2000.0,
    "kar": 1200.0,
    "satir_komisyon": 0.0,
    "kargo_fiyat": 0.0,
    "siparis_durumu": "aktif",
    "magaza": "sporsuit",
    "pazaryeri": "Perakende",
    "musteri_adi": "-",
    "urun_adi": "-",
    "key": "TP_MANUEL|SPRS-TEST-001"
}])

# Eksik kolonları tamamla
for col in df.columns:
    if col not in manuel_veri.columns:
        manuel_veri[col] = 0

# Kolon sırasını eşitle
manuel_veri = manuel_veri[df.columns]

# 🔁 Verilere manuel veriyi de ekle
df = pd.concat([df, manuel_veri], ignore_index=True)


# Verileri birleştir
df = pd.concat([df, toptan_df], ignore_index=True)

# Normalize edilmiş mağaza sütununu uygula
df["magaza_normalized"] = df["magaza"].apply(normalize_magaza)

# -------------------- İADELER --------------------
iade_df = pd.read_excel("İadeler.xlsx")
iade_df.columns = [c.strip() for c in iade_df.columns]
iade_df["siparis_tarihi"] = pd.to_datetime(iade_df["İade Tarihi"], format="%d.%m.%Y %H:%M", errors="coerce").dt.date


iade_df["key"] = iade_df["Sipariş No"].astype(str) + "|" + iade_df["Stok Kodu"].astype(str)
df["key"] = df["Sipariş No"].astype(str) + "|" + df["Stok Kodu"].astype(str)

# Eşleşen iadelerin karlarını sıfırla
df.loc[df["key"].isin(iade_df["key"]), "kar"] = 0.0

# -------------------- MAĞAZA LİSTESİ GÜNCELLE --------------------
st.session_state["tum_magaza_listesi"] = ["Sporsuit", "LATTE", "Depoba", "İLYAKİ", "AIDA HOME", "Perakende"]

# GÜNCELLENEN: Pivot tablolar ve özetlerde "perakende" de gözüksün diye listeyi normalize ekle
magazalar = ["sporsuit", "latte", "depoba", "ilyaki", "aida home", "perakende"]

# -------------------- FİLTRELER --------------------
# -------------------- SIDEBAR FİLTRELERİ (DÜZENLİ BLOKLAR) --------------------
with st.sidebar:
    st.markdown("## 📊 Filtreleme Paneli")

    # ---- TARİH FİLTRESİ ----
    st.markdown("### 📅 Tarih Filtresi")
    filtre_tipi = st.radio("Filtre Tipi Seç", ["Tarih Aralığı", "Dönem Bazlı"])

    if filtre_tipi == "Tarih Aralığı":
        tarih_aralik = st.date_input(
            "Tarih Aralığı Seç",
            [df["siparis_tarihi"].min().date(), df["siparis_tarihi"].max().date()]
        )
        donem = None
    else:
        tarih_aralik = None
        yil_min = df["siparis_tarihi"].dt.year.min()
        yil_max = datetime.datetime.now().year
        yillar = list(range(int(yil_min), int(yil_max) + 1))
        aylar = list(range(1, 13))
        ay_isimleri = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                       "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        secilen_yil = st.selectbox("🗓️ Yıl Seç", yillar, index=len(yillar) - 1, key="sidebar_yil")
        secilen_ay = st.selectbox("📆 Ay Seç", ay_isimleri, index=datetime.datetime.now().month - 1, key="sidebar_ay")

        donem = f"{secilen_yil}-{aylar[ay_isimleri.index(secilen_ay)]:02d}"

    # ---- MAĞAZA FİLTRESİ ----
    st.markdown("### 🏢 Firma Filtresi")
    verideki_magazalar = df["magaza_normalized"].dropna().unique().tolist()
    sabit_magazalar = ["sporsuit", "latte", "depoba", "ilyaki", "aida home"]
    tum_magazalar = sorted(set(verideki_magazalar + sabit_magazalar))
    secilen_magazalar = st.multiselect("Firma Seç", options=tum_magazalar, default=tum_magazalar)

    # ---- PAZARYERİ FİLTRESİ ----
    st.markdown("### 🛍️ Pazaryeri Filtresi")
    secilen_pazaryerleri = st.multiselect(
        "Pazaryeri Seç",
        options=["Amazon", "Trendyol", "PrestaShop", "Hepsiburada", "N11", "Perakende"],
        default=["Amazon", "Trendyol", "PrestaShop", "Hepsiburada", "N11", "Perakende"]
    )
df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_")
              .replace("ç", "c").replace("ş", "s").replace("ğ", "g")
              .replace("ü", "u").replace("ı", "i").replace("ö", "o") for c in df.columns]

# 2. Tarih filtresini uygula
# 2. Tarih filtresini uygula
if filtre_tipi == "Tarih Aralığı":
    baslangic, bitis = tarih_aralik
    df_filtered = df[
        (df["siparis_tarihi"].dt.date >= baslangic) &
        (df["siparis_tarihi"].dt.date <= bitis)
    ]
    iade_df = iade_df[
        (iade_df["siparis_tarihi"] >= baslangic) &
        (iade_df["siparis_tarihi"] <= bitis)
    ]
else:
    donem = f"{secilen_yil}-{aylar[ay_isimleri.index(secilen_ay)]:02d}"
    df_filtered = df[df["siparis_tarihi"].dt.strftime("%Y-%m") == donem]
    iade_df = iade_df[
        iade_df["siparis_tarihi"].apply(lambda d: d.strftime("%Y-%m") == donem if pd.notnull(d) else False)
    ]

sayisal_kolonlar = [
    "satir_fiyat",
    "urun_toplam_maliyet",
    "satir_komisyon",
    "satir_kargo_fiyat"
]

def temizle_sayisal_kolon(df, kolon_adi):
    if kolon_adi not in df.columns:
        df[kolon_adi] = 0.0
    else:
        df[kolon_adi] = (
            df[kolon_adi]
            .astype(str)
            .str.replace("₺", "", regex=False)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        df[kolon_adi] = pd.to_numeric(df[kolon_adi], errors="coerce").fillna(0)
    return df

for kolon in ["satir_fiyat", "urun_toplam_maliyet", "satir_komisyon", "satir_kargo_fiyat"]:
    df_filtered = temizle_sayisal_kolon(df_filtered, kolon)

df_filtered["kar"] = (
    df_filtered["satir_fiyat"]
    - df_filtered["urun_toplam_maliyet"]
    - df_filtered["satir_komisyon"]
    - df_filtered["satir_kargo_fiyat"]
)

# 3. Artık 'fatura_il' kolonu varsa düzenle
if "fatura_il" in df_filtered.columns:
    df_filtered["fatura_il"] = df_filtered["fatura_il"].astype(str).str.strip().str.title()
elif "fatura_-_il" in df_filtered.columns:
    df_filtered.rename(columns={"fatura_-_il": "fatura_il"}, inplace=True)
    df_filtered["fatura_il"] = df_filtered["fatura_il"].astype(str).str.strip().str.title()
else:
    df_filtered["fatura_il"] = "Bilinmiyor"

df_filtered["satir_fiyat"] = pd.to_numeric(df_filtered["satir_fiyat"], errors="coerce").fillna(0)
df_filtered["kar"] = pd.to_numeric(df_filtered["kar"], errors="coerce").fillna(0)
df_filtered["urun_toplam_maliyet"] = pd.to_numeric(df_filtered["urun_toplam_maliyet"], errors="coerce").fillna(0)

# 4. İl bazında özet veriyi oluştur
il_ozet = df_filtered.groupby("fatura_il").agg({
    "satir_fiyat": "sum",
    "kar": "sum"
}).reset_index().rename(columns={
    "fatura_il": "il",
    "satir_fiyat": "Toplam Ciro",
    "kar": "Net Kâr"
})


# --------------------
# 📦 Ürün Stok Durumu
urunler_df = pd.read_excel("Urunler.xlsx")
urunler_df.columns = [
    c.strip().lower()
    .replace(" ", "_")
    .replace("-", "_")
    .replace("ç", "c").replace("ş", "s").replace("ğ", "g")
    .replace("ü", "u").replace("ı", "i").replace("ö", "o")
    for c in urunler_df.columns
]

urunler_df["stok"] = pd.to_numeric(urunler_df["stok"], errors="coerce").fillna(0)

stokta_olmayan_sayi = (urunler_df["stok"] <= 0).sum()
kritik_stok_sayi = (urunler_df["stok"] <= 1).sum()

st.markdown("### 📦 Stok Durumu Özeti")
col_stok1, col_stok2 = st.columns(2)
col_stok1.metric("🛑 Stokta Olmayan Ürün", stokta_olmayan_sayi)
col_stok2.metric("⚠️ Kritik Stok (<=1)", kritik_stok_sayi)

# Eksik illeri sıfır değerle dataframe'e ekle
geo_iller = [feature["properties"]["name"] for feature in turkiye_geojson["features"]]
mevcut_iller = il_ozet["il"].tolist()
eksik_iller = list(set(geo_iller) - set(mevcut_iller))

eksik_df = pd.DataFrame({
    "il": eksik_iller,
    "Toplam Ciro": 0,
    "Net Kâr": 0
})

il_ozet = pd.concat([il_ozet, eksik_df], ignore_index=True)

# -------------------- HARİTALARI YAN YANA VE ZOOM KAPALI --------------------
st.markdown("### 🌍 İl Bazında Ciro ve Kâr Dağılımı")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Ciro Haritası")
    fig_ciro = px.choropleth(
        il_ozet,
        geojson=turkiye_geojson,
        featureidkey="properties.name",
        locations="il",
        color="Toplam Ciro",
        color_continuous_scale="Blues",
        labels={"Toplam Ciro": "₺"},
    )
    fig_ciro.update_geos(fitbounds="locations", visible=False)
    fig_ciro.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        dragmode=False  # 👈 Scroll ile zoom kapalı
    )
    st.plotly_chart(fig_ciro, use_container_width=True)

with col2:
    st.subheader("📈 Net Kâr Haritası")
    fig_kar = px.choropleth(
        il_ozet,
        geojson=turkiye_geojson,
        locations="il",
        featureidkey="properties.name",
        color="Net Kâr",
        color_continuous_scale="Greens",
        labels={"Net Kâr": "₺"},
        hover_name="il"
    )
    fig_kar.update_geos(fitbounds="locations", visible=False)
    fig_kar.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        dragmode=False  # 👈 Scroll ile zoom kapalı
    )
    st.plotly_chart(fig_kar, use_container_width=True)

# --------------------
# MAĞAZA / PAZARYERİ FİLTRESİ
# --------------------
df_filtered = df_filtered[
    (df_filtered["magaza_normalized"].isin(secilen_magazalar)) &
    (df_filtered["pazaryeri"].isin(secilen_pazaryerleri))
    ]

# Normalize edilmiş mağaza sütununu tekrar uygula (gerekirse)
df["magaza_normalized"] = df["magaza"].apply(normalize_magaza)

# 🔢 Sipariş Türleri
toplam_siparis = len(df_filtered)
iptal_sayisi = df_filtered[df_filtered["siparis_satir_durumu"].str.lower() == "iptal"].shape[0]
iade_sayisi = iade_df.shape[0]
aktif_siparis = toplam_siparis - iptal_sayisi - iade_sayisi

# 📦 Temel Sipariş Göstergeleri
st.markdown("### 📦 Sipariş ve Satış Özeti")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📦 Toplam Sipariş", toplam_siparis)
col2.metric("✅ Aktif Sipariş", aktif_siparis)
col3.metric("↩️ İade", iade_sayisi, delta=f"%{(iade_sayisi / toplam_siparis * 100):.2f}" if toplam_siparis else "0%")
col4.metric("❌ İptal", iptal_sayisi, delta=f"%{(iptal_sayisi / toplam_siparis * 100):.2f}" if toplam_siparis else "0%")

# 💰 Ciro ve Kâr
col5, col6, col7, col8 = st.columns(4)
col5.metric("💰 Toplam Ciro", f"{df_filtered['satir_fiyat'].sum():,.2f} ₺")
col6.metric("📈 Net Kâr", f"{df_filtered['kar'].sum():,.2f} ₺")
col7.metric("🛒 Ortalama Sepet", f"{df_filtered['satir_fiyat'].mean():,.2f} ₺")
col8.metric("📌 Ortalama Kâr", f"{df_filtered['kar'].mean():,.2f} ₺")

# 📉 Maliyet ve Kesintiler
col9, col10, col11, col12 = st.columns(4)
col9.metric("📉 Ortalama Maliyet", f"{df_filtered['urun_toplam_maliyet'].mean():,.2f} ₺")
col10.metric("📊 Komisyon Tutarı", f"{df_filtered['satir_komisyon'].sum():,.2f} ₺")
col11.metric("🚚 Kargo Tutarı", f"{df_filtered['satir_kargo_fiyat'].sum():,.2f} ₺")



# 📊 Mağaza - Pazaryeri Özeti
st.markdown("### 🧾 Mağaza & Pazaryeri Satış Özeti")

# Tüm mağazaların sabit listesi (veri olmasa bile görünsün)
tum_magaza_listesi = ["Sporsuit", "LATTE", "Depoba", "İLYAKİ", "AIDA HOME"]
tum_magazalar = [m.strip().lower().replace("ı", "i").capitalize() for m in tum_magaza_listesi]

# Tüm pazaryerlerini veriden al
# df["magaza_normalized"] = df["magaza"].astype(str).str.strip().str.lower().replace("ı", "i").str.capitalize()
df["pazaryeri"] = df["pazaryeri"].astype(str).str.strip()
tum_pazaryerleri = sorted(df["pazaryeri"].unique())

# # Pivot: Satır Fiyat
# pivot_fiyat = pd.pivot_table(
#     df,
#     index="magaza_normalized",
#     columns="pazaryeri",
#     values="satir_fiyat",
#     aggfunc="sum",
#     fill_value=0
# )
# pivot_fiyat = pivot_fiyat.reindex(index=tum_magazalar, columns=tum_pazaryerleri, fill_value=0)
# pivot_fiyat.columns = [f"{col} - Satır Fiyat" for col in pivot_fiyat.columns]
#
# # Pivot: Komisyon
# pivot_komisyon = pd.pivot_table(
#     df,
#     index="magaza_normalized",
#     columns="pazaryeri",
#     values="satir_komisyon",
#     aggfunc="sum",
#     fill_value=0
# )
# pivot_komisyon = pivot_komisyon.reindex(index=tum_magazalar, columns=tum_pazaryerleri, fill_value=0)
# pivot_komisyon.columns = [f"{col} - Komisyon" for col in pivot_komisyon.columns]
#
# # Birleştir
# summary_full = pd.concat([pivot_fiyat, pivot_komisyon], axis=1).reset_index()
# summary_full.rename(columns={"magaza_normalized": "Mağaza"}, inplace=True)
#
# # Göster
# st.dataframe(summary_full, use_container_width=True)
# 🎯 Pazaryeri ve metrik yapısı
sabit_pazaryerleri = ["Amazon", "Trendyol", "PrestaShop", "Hepsiburada", "N11", "Perakende"]
metrikler = ["Satış", "Gider", "Kar"]
magazalar = ["sporsuit", "latte", "depoba", "ilyaki", "aida home"]

# Pivotlar
pivot_satis = pd.pivot_table(df_filtered, index="magaza_normalized", columns="pazaryeri", values="satir_fiyat", aggfunc="sum", fill_value=0)
pivot_kar = pd.pivot_table(df_filtered, index="magaza_normalized", columns="pazaryeri", values="kar", aggfunc="sum", fill_value=0)

# Gider = maliyet + komisyon + kargo
pivot_maliyet = pd.pivot_table(df_filtered, index="magaza_normalized", columns="pazaryeri", values="urun_toplam_maliyet", aggfunc="sum", fill_value=0)
pivot_komisyon = pd.pivot_table(df_filtered, index="magaza_normalized", columns="pazaryeri", values="satir_komisyon", aggfunc="sum", fill_value=0)
pivot_kargo = pd.pivot_table(df_filtered, index="magaza_normalized", columns="pazaryeri", values="satir_kargo_fiyat", aggfunc="sum", fill_value=0)
pivot_gider = pivot_maliyet.add(pivot_komisyon, fill_value=0).add(pivot_kargo, fill_value=0)

# Boş DataFrame
columns = pd.MultiIndex.from_product([sabit_pazaryerleri + ["Toplam"], metrikler])
df_multi = pd.DataFrame(index=magazalar, columns=columns, dtype="float").fillna(0.0)

# Verileri doldur
for pazaryeri in sabit_pazaryerleri:
    for magaza in magazalar:
        m = magaza
        s = pivot_satis.at[m, pazaryeri] if m in pivot_satis.index and pazaryeri in pivot_satis.columns else 0
        g = pivot_gider.at[m, pazaryeri] if m in pivot_gider.index and pazaryeri in pivot_gider.columns else 0
        k = pivot_kar.at[m, pazaryeri]   if m in pivot_kar.index and pazaryeri in pivot_kar.columns else 0

        df_multi.loc[m, (pazaryeri, "Satış")] = s
        df_multi.loc[m, (pazaryeri, "Gider")] = g
        df_multi.loc[m, (pazaryeri, "Kar")] = k

# --- 📊 Mağaza & Pazaryeri Satış Özeti (GÜNCELLENMİŞ) ---

# Toplam kolonları
df_multi[("Toplam", "Satış")] = df_multi.loc[:, pd.IndexSlice[:, "Satış"]].sum(axis=1)
df_multi[("Toplam", "Gider")] = df_multi.loc[:, pd.IndexSlice[:, "Gider"]].sum(axis=1)
df_multi[("Toplam", "Kar")] = df_multi.loc[:, pd.IndexSlice[:, "Kar"]].sum(axis=1)
# 1. Mağaza'yı index'ten çıkar, başa al
df_multi_reset = df_multi.copy().reset_index()

# 2. MultiIndex yerine düz string başlıklar oluştur
df_multi_reset.columns = ["Mağaza"] + [f"{pazaryeri} - {metrik}" for pazaryeri, metrik in df_multi.columns]


# 2. Yeni başlıkları hizalı tanımla
new_columns = [("Mağaza", "")] + list(df_multi.columns)
df_multi_reset.columns = pd.MultiIndex.from_tuples(new_columns)

# 3. Sayısal kolonları seç
numeric_cols = df_multi_reset.select_dtypes(include='number').columns

# 4. Stil ve render
html_table = (
    df_multi_reset.style
    .format({col: "{:,.2f}" for col in numeric_cols})
    .set_table_styles([
        {
            'selector': 'thead th',
            'props': [
                ('text-align', 'center'),
                ('vertical-align', 'middle'),
                ('font-size', '13px'),
                ('padding', '4px'),
                ('border-bottom', '1px solid #ccc')
            ]
        },
        {
            'selector': 'tbody td',
            'props': [
                ('text-align', 'center'),
                ('font-size', '13px'),
                ('padding', '4px')
            ]
        }
    ])
    .set_properties(**{'text-align': 'center'})
    .to_html(index=False)
)

# 5. CSS ve tabloyu bastır
st.markdown(f"""
<style>
table {{
    border-collapse: collapse;
    width: 100%;
}}

th, td {{
    padding: 4px;
    white-space: nowrap;
    text-align: center;
}}

thead th {{
    font-weight: bold;
    vertical-align: middle;
}}

.block-container {{
    padding-top: 0.5rem;
}}
</style>

{html_table}
""", unsafe_allow_html=True)

# GRAFİKLER


st.markdown("### 📈 Günlük Ciro & Net Kâr")

# Günlük veriyi hazırla
daily = df_filtered.groupby(df_filtered["siparis_tarihi"].dt.date).agg({
    "satir_fiyat": "sum",
    "kar": "sum"
}).rename(columns={"satir_fiyat": "Toplam Ciro", "kar": "Net Kâr"}).reset_index()

daily["Tarih"] = pd.to_datetime(daily["siparis_tarihi"])

# Uzun formata çevir
daily_melted = daily.melt(
    id_vars="Tarih",
    value_vars=["Toplam Ciro", "Net Kâr"],
    var_name="Gösterge",
    value_name="Tutar"
)

# Altair grafik
chart = alt.Chart(daily_melted).mark_line(point=True).encode(
    x=alt.X("Tarih:T", title="Tarih", axis=alt.Axis(format="%d %b", labelAngle=0)),
    y=alt.Y("Tutar:Q", title="Tutar (₺)"),
    color=alt.Color("Gösterge:N", title="Gösterge"),
    tooltip=[
        alt.Tooltip("Tarih:T", title="Tarih", format="%d %B %Y"),
        alt.Tooltip("Gösterge:N", title="Gösterge"),
        alt.Tooltip("Tutar:Q", title="Tutar (₺)")
    ]
).properties(
    height=400,
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_legend(
    titleFontSize=13,
    labelFontSize=12,
    orient='bottom'
).configure_title(
    fontSize=20,
    anchor='start',
    font='Segoe UI'
)

# Streamlit'te düzgün yerleşimle göster
st.altair_chart(chart, use_container_width=True)

# Pazaryerine göre gruplama
grup = df_filtered.groupby("pazaryeri").agg({
    "satir_fiyat": "sum",
    "kar": "sum",
    "satir_kargo_fiyat": "sum",
    "satir_komisyon": "sum"
}).reset_index().rename(columns={
    "satir_fiyat": "Toplam Ciro",
    "kar": "Net Kâr",
    "satir_kargo_fiyat": "Kargo Tutarı",
    "satir_komisyon": "Komisyon Tutarı"
})

st.markdown("### 🏷️ Pazaryerine Göre Ciro, Kâr, Komisyon, Kargo")

col12, col13 = st.columns(2)

with col12:
    st.subheader("💰 Ciro ve Kâr")

    fig_ciro = px.bar(
        grup,
        x="pazaryeri",
        y="Toplam Ciro",
        title="Toplam Ciro",
        text_auto=".2s",
        labels={"pazaryeri": "Pazaryeri", "Toplam Ciro": "₺"}
    )
    fig_ciro.update_layout(dragmode=False)  # 👈 Zoom ve pan kapalı
    st.plotly_chart(fig_ciro, use_container_width=True)

    fig_kar = px.bar(
        grup,
        x="pazaryeri",
        y="Net Kâr",
        title="Net Kâr",
        text_auto=".2s",
        labels={"pazaryeri": "Pazaryeri", "Net Kâr": "₺"}
    )
    fig_kar.update_layout(dragmode=False)
    st.plotly_chart(fig_kar, use_container_width=True)

with col13:
    st.subheader("📦 Kargo & Komisyon")

    fig_kargo = px.bar(
        grup,
        x="pazaryeri",
        y="Kargo Tutarı",
        title="Kargo Tutarı",
        text_auto=".2s",
        labels={"pazaryeri": "Pazaryeri", "Kargo Tutarı": "₺"}
    )
    fig_kargo.update_layout(dragmode=False)
    st.plotly_chart(fig_kargo, use_container_width=True)

    fig_komisyon = px.bar(
        grup,
        x="pazaryeri",
        y="Komisyon Tutarı",
        title="Komisyon Tutarı",
        text_auto=".2s",
        labels={"pazaryeri": "Pazaryeri", "Komisyon Tutarı": "₺"}
    )
    fig_komisyon.update_layout(dragmode=False)
    st.plotly_chart(fig_komisyon, use_container_width=True)