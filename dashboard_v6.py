import streamlit as st
import pandas as pd
import datetime
import altair as alt
import unicodedata
import json
import geopandas as gpd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from matplotlib.colors import to_rgb



st.set_page_config(page_title="Satış Dashboard", layout="wide")

st.markdown("""
<style>
section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"] {
    background-color: #0c1022 !important;
    border: 1px solid #00c3ff !important;
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 13px;
    margin: 4px 4px 4px 0;
    color: white !important;
    font-weight: 500;
}

/* X butonunu küçük yap ve hizala */
section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"] button {
    background-color: transparent !important;
    color: #ff7675 !important;
    font-weight: bold;
    margin-left: 6px;
}

/* Seçili kutulara hover efekti */
section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"]:hover {
    background-color: #1f2c3f !important;
    border-color: #00c3ff !important;
}

label.css-1w0j46c, label.css-1y4p8pa { 
    font-size: 15px !important;
    color: #ecf0f1 !important;
    padding-left: 8px;
}
.st-emotion-cache-tj3uvl {
    padding: 0px calc(2px + 1rem) 19rem;
    margin-top: -14%;
}
.st-de {
    border-left-color: #0c1022 !important;
}
.st-av {
    background-color: #0c1022 !important;
}
.st-df {
    border-right-color: #0c1022 !important;
}
.st-dg {
    border-top-color: #0c1022 !important;
}
.st-dh {
    border-bottom-color: #0c1022 !important;
}
/* Sidebar arka planı ve genel yazı rengi */
section[data-testid="stSidebar"] > div:first-child {
    overflow: hidden !important;
    height: 100% !important;
}
html, .main, .block-container {
    background-color: #0c1022 !important;
    color: #ffffff !important;
}
.st-emotion-cache-1v0mbdj, .st-emotion-cache-10trblm,
.st-emotion-cache-1y4p8pa, .st-emotion-cache-1w0j46c {
    color: #ffffff !important;
}
section[data-testid="stSidebar"] {
    background-color: #0c1022 !important;
    color: white !important;
}

/* Tarih seçim açılır pencere (takvim) arka planı */
div[role="dialog"] {
    background-color: #1e1e1e !important;
    color: white !important;
    border-radius: 8px;
    padding: 10px;
}

/* Takvim içindeki günler */
div[role="dialog"] td {
    color: white !important;
}

/* Seçili tarih yuvarlak görünümünü değiştir */
div[role="dialog"] td > div[aria-selected="true"] {
    background-color: #00cec9 !important;
    color: black !important;
    border-radius: 20px !important;
}

/* Hover efekti */
div[role="dialog"] td:hover {
    background-color: #3d3d3d !important;
    border-radius: 20px;
}

section[data-testid="stSidebar"] .stDateInput input {
    border-radius: 6px;
    padding: 6px 46px 6px 61px;
    font-size: 13px;
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
section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] select,
 section[data-testid="stSidebar"] textarea, 
 section[data-testid="stSidebar"] .stMultiSelect,
  section[data-testid="stSidebar"] .stDateInput, 
  section[data-testid="stSidebar"] .stTextInput,
   section[data-testid="stSidebar"] .stSelectbox {
    /* background-color: #2c2c2c !important; */
    color: rgba(0, 0, 0, 0.75) !important;
    /* border: 1px solid #444 !important; */
    border-radius: 5px;
}
section[data-testid="stSidebar"] select,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] .stMultiSelect,
section[data-testid="stSidebar"] .stDateInput,
section[data-testid="stSidebar"] .stTextInput,
section[data-testid="stSidebar"] .stSelectbox {
    /* background-color: #2c2c2c !important; */
    color: rgba(0, 0, 0, 0.75) !important;
    /* border: 1px solid #444 !important; */
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
.st-h0::after {
    background-color: #2c2c2c;
}

/* Kenarlıkların rengini siyah yap */
.st-h0::after,
.st-h1::after,
.st-h2::after,
.st-h3::after,
.st-h4::after,
.st-h5::after,
.st-h6::after,
.st-ci,
.st-cf,f
.st-cg,
.st-ch {
    border-color: #000000 !important;
    border-top-color: #000000 !important;
    border-bottom-color: #000000 !important;
    border-left-color: #000000 !important;
    border-right-color: #000000 !important;
}
.st-emotion-cache-13lcgu3 {
    display: inline-flex
;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 2.5rem;
    margin: 0px;
    line-height: 1.6;
    text-transform: none;
    font-size: inherit;
    font-family: inherit;
    color: inherit;
    width: 221%;
    cursor: pointer;
    user-select: none;
    background-color: transparent;
    border: 1px solid rgba(49, 51, 63, 0.2);
    color: white;
}
</style>
""", unsafe_allow_html=True)



# --------------------
# GÖMÜLÜ CSS
# --------------------
st.markdown("""
<style>
body {  
    background-color: #0c1022 !important;
    color: #ffffff; 
}
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
    /* Bütün expander başlık kutucukları */
    div[data-testid="stExpander"] > div:first-child  {
        width: 160px;        /* istediğin genişlik */
        margin-left: auto;   /* sağa yasla */
        margin-top: 4px;     /* gauge ile arasında boşluk */
    }
/* Dark arka-plan + primary renklere ince ayar  */
    .stApp { background-color:#0c1222; color:#FFFFFF; }
    /* Segmeli radyo butonlarını "toggle" gibi göster */
    div[data-baseweb="radio"] > div { flex-direction:row; }
    div[data-baseweb="radio"] label span {
        background:#132138; padding:4px 18px; border-radius:6px; margin-right:6px;
        font-weight:600; color:#d0d0d0; cursor:pointer;
        transition:all .2s ease-in-out;
    }
    /* Seçili durum: beyaz zemin koyu metin  */
    div[data-baseweb="radio"] input:checked + label span {
        background:#FFFFFF; color:#0c1222;
    }
    /* Plotly renk çubuğunu ince gösterelim */
    .js-plotly-plot .colorbar { width:10px!important; }
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

def interpolate_colors(start_hex, end_hex, n):
    if n <= 0:
        return []
    start_rgb = np.array(to_rgb(start_hex))
    end_rgb = np.array(to_rgb(end_hex))
    return [f'rgb({int(r*255)}, {int(g*255)}, {int(b*255)})'
            for r, g, b in np.linspace(start_rgb, end_rgb, n)]



def plot_gauge_gradient(value, label, base_colors, global_max, adet_max=25, total_slices=50):
    if any(x in label.lower() for x in ["kâr", "komisyon", "ciro", "kargo", "maliyet", "tutar"]):
        max_val = global_max if global_max > 0 else 1
    else:
        max_val = min(adet_max, global_max * 1.1) if global_max > 0 else adet_max

    percentage = (value / max_val) * 100 if max_val != 0 else 0
    filled_slices = max(0, int((percentage / 100) * total_slices))
    empty_slices = total_slices - filled_slices

    gradient_colors = interpolate_colors(base_colors[0], base_colors[1], filled_slices)
    pie_colors = gradient_colors + ["#2c3e50"] * empty_slices

    if any(x in label.lower() for x in ["kâr", "komisyon", "ciro", "kargo", "maliyet", "tutar"]):
        formatted_value = f"{value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".") + " ₺"
    else:
        formatted_value = f"{int(value):,}".replace(",", ".") + " adet"

    fig = go.Figure()
    fig.add_trace(go.Pie(
        values=[1] * total_slices,
        hole=0.75,
        direction='clockwise',
        sort=False,
        marker=dict(colors=pie_colors, line=dict(color="#0c1022", width=1)),
        textinfo='none',
        hoverinfo='skip'
    ))

    fig.update_layout(
        paper_bgcolor="#0c1022",
        margin=dict(l=0, r=0, t=5, b=5),
        height=160,
        width=160,
        showlegend=False,
        annotations=[dict(
            text=f'<b>{formatted_value}</b><br><span style="font-size:13px; color:#aaa">{label}</span>',
            x=0.5, y=0.5, font_size=13, showarrow=False
        )]
    )

    return fig


@st.cache_data(show_spinner=False)
def cached_plot_gauge_gradient(value, label, base_colors, global_max, adet_max=25, total_slices=30):
    return plot_gauge_gradient(value, label, base_colors, global_max, adet_max, total_slices)


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
    st.markdown("## Dashboard")
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
        secilen_ay = st.selectbox("📆 Ay Seç", ay_isimleri, index=datetime.datetime.now().month - 1,
                                  key="sidebar_ay")

        donem = f"{secilen_yil}-{aylar[ay_isimleri.index(secilen_ay)]:02d}"
    # ---------------- Mağaza Checkbox (Pazaryerinin Altında) ----------------
    st.markdown("### 🏬 Mağaza Seçiniz")
    tum_magazalar = ["sporsuit", "latte", "depoba", "ilyaki", "aida home", "perakende"]
    secilen_magazalar = []
    cols = st.columns(2)
    for i, magaza in enumerate(tum_magazalar):
        col = cols[i % 2]
        with col:
            if st.checkbox(magaza.title(), value=True, key=f"magaza_{magaza}"):
                secilen_magazalar.append(magaza)

    # ---------------- Pazaryeri Checkbox 2'li ----------------
    st.markdown("### 🛍️ Pazaryeri Seçiniz")

    tum_pazaryerleri = ["Amazon", "Trendyol", "PrestaShop", "Hepsiburada", "N11", "Perakende"]
    secilen_pazaryerleri = []
    cols = st.columns(2)
    for i, pazar in enumerate(tum_pazaryerleri):
        col = cols[i % 2]
        with col:
            if st.checkbox(pazar, value=True, key=f"pazaryeri_{pazar}"):
                secilen_pazaryerleri.append(pazar)

df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_")
              .replace("ç", "c").replace("ş", "s").replace("ğ", "g")
              .replace("ü", "u").replace("ı", "i").replace("ö", "o") for c in df.columns]

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
base_colors = ("#00b2ff", "#00ffb3")

# Metrikler
metric_cards = [
    {"label": "Toplam Sipariş", "value": toplam_siparis},
    {"label": "Aktif Sipariş", "value": aktif_siparis},
    {"label": "İade", "value": iade_sayisi},
    {"label": "İptal", "value": iptal_sayisi},
    {"label": "Toplam Ciro", "value": df_filtered["satir_fiyat"].sum()},
    {"label": "Net Kâr", "value": df_filtered["kar"].sum()},
    {"label": "Komisyon", "value": df_filtered["satir_komisyon"].sum()},
    {"label": "Kargo", "value": df_filtered["satir_kargo_fiyat"].sum()},
]

# Renk geçiş fonksiyonu
def interpolate_colors(start_hex, end_hex, n):
    start_rgb = np.array(to_rgb(start_hex))
    end_rgb = np.array(to_rgb(end_hex))
    return [f'rgb({int(r*255)}, {int(g*255)}, {int(b*255)})' for r, g, b in np.linspace(start_rgb, end_rgb, n)]

# Gauge oluşturma
def plot_gauge_gradient(value, label, base_colors, global_max, adet_max=25, total_slices=50):
    is_tutar = any(x in label.lower() for x in ["kâr", "komisyon", "ciro", "kargo"])
    max_val = global_max\
        if is_tutar else min(adet_max, global_max * 1.1)
    percentage = (value / max_val) * 100 if max_val != 0 else 0
    filled_slices = max(0, int((percentage / 100) * total_slices))
    empty_slices = total_slices - filled_slices
    gradient_colors = interpolate_colors(base_colors[0], base_colors[1], filled_slices)
    pie_colors = gradient_colors + ["#2c3e50"] * empty_slices

    formatted_value = (
        f"{value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".") + " ₺"
        if is_tutar else f"{int(value):,}".replace(",", ".") + " adet"
    )

    fig = go.Figure(go.Pie(
        values=[1] * total_slices,
        hole=0.75,
        direction='clockwise',
        sort=False,
        marker=dict(colors=pie_colors, line=dict(color="#0c1022", width=1)),
        textinfo='none',
        hoverinfo='skip'
    ))
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=160, width=160,
        paper_bgcolor="#0c1022",
        annotations=[dict(
            text=f'<b>{formatted_value}</b><br><span style="font-size:13px; color:#aaa">{label}</span>',
            x=0.5, y=0.5, showarrow=False
        )]
    )
    return fig

# ───────── Kompakt Detay Fonksiyonu ─────────

def draw_metric_detail_v2(df_filtered, label, iade_df=None):
    df_data = df_filtered.copy()

    # İade metriklerinde iade_df ile eşleşme
    if label == "İade" and iade_df is not None:
        # Kolonları yeniden adlandır (zaten adlandırılmışsa tekrar etmez)
        iade_df = iade_df.rename(columns={
            "Sipariş No": "siparis_no",
            "Pazaryeri": "pazaryeri",
            "Mağaza": "magaza"
        })

        # Dtype eşitle
        iade_df["siparis_no"] = iade_df["siparis_no"].astype(str)
        df_filtered["siparis_no"] = df_filtered["siparis_no"].astype(str)

        # Merge işlemi
        df_data = df_filtered.merge(
            iade_df[["siparis_no", "pazaryeri", "magaza"]],
            on="siparis_no", how="left"
        )

        if "pazaryeri" in df_data.columns:
            df_data["pazaryeri"] = df_data["pazaryeri"].fillna("Bilinmeyen")
        else:
            df_data["pazaryeri"] = "Bilinmeyen"

        if "magaza" in df_data.columns:
            df_data["magaza"] = df_data["magaza"].fillna("Bilinmeyen")
        else:
            df_data["magaza"] = "Bilinmeyen"

    # Filtreleme
    if label == "Aktif Sipariş":
        df_data = df_data[df_data["siparis_satir_durumu"].str.lower() == "aktif"]
    elif label == "İptal":
        iptal_df = df_filtered[df_filtered["siparis_satir_durumu"].str.lower() == "iptal"].copy()

        if not iptal_df.empty:
            # Mağaza bazlı bar chart
            tmp_magaza = (
                iptal_df.groupby("magaza_normalized")
                .size().reset_index(name="adet")
                .sort_values("adet", ascending=False)
            )

            fig_left = px.bar(tmp_magaza, x="adet", y="magaza_normalized", orientation="h",
                              color_discrete_sequence=["#fab1a0"])

            # Pazaryeri bazlı pie chart
            tmp_pazar = (
                iptal_df["pazaryeri"]
                .value_counts(normalize=True)
                .rename("oran")
                .reset_index()
                .rename(columns={"index": "pazaryeri"})
            )
            tmp_pazar["oran"] *= 100

            fig_right = px.pie(tmp_pazar, names="pazaryeri", values="oran", hole=0.6,
                               color_discrete_sequence=["#ff7675", "#fd79a8", "#e17055"])
            fig_right.update_layout(showlegend=False)
            if not tmp_pazar.empty:
                fig_right.update_layout(
                    annotations=[
                        dict(text=f"<b>{tmp_pazar.iloc[0]['pazaryeri']}</b><br>{tmp_pazar.iloc[0]['oran']:.0f}%",
                             x=0.5, y=0.5, showarrow=False)]
                )
        else:
            fig_left = go.Figure()
            fig_right = go.Figure()
    elif label == "İade" and iade_df is not None:
        # Gerekli kolonları yeniden adlandıralım
        iade_df = iade_df.rename(columns={
            "Pazaryeri": "pazaryeri",
            "Mağaza": "magaza"
        })

        iade_df["pazaryeri"] = iade_df["pazaryeri"].fillna("Bilinmeyen")
        iade_df["magaza"] = iade_df["magaza"].fillna("Bilinmeyen")

        # Mağazaya göre iade sayısı (SOL GRAFİK)
        tmp_magaza = (
            iade_df.groupby("magaza")
            .size().reset_index(name="adet")
            .sort_values("adet", ascending=False)
        )

        fig_left = px.bar(tmp_magaza, x="adet", y="magaza", orientation="h",
                          color_discrete_sequence=["#00bfff"])
        fig_left.update_layout(
            height=220,
            paper_bgcolor="#0c1022",
            plot_bgcolor="#0c1022",
            font=dict(color="white"),
            margin=dict(l=0, r=0, t=20, b=10)
        )

        # Pazaryerine göre iade oranı (SAĞ GRAFİK)
        tmp_pazar = (
            iade_df["pazaryeri"]
            .value_counts(normalize=True)
            .rename("oran")
            .reset_index()
            .rename(columns={"index": "pazaryeri"})
        )
        tmp_pazar["oran"] *= 100

        if not tmp_pazar.empty:
            fig_right = px.pie(tmp_pazar, names="pazaryeri", values="oran", hole=0.6,
                               color_discrete_sequence=["#00ffc3", "#00b2ff", "#1e90ff"])
            fig_right.update_layout(
                height=220,
                paper_bgcolor="#0c1022",
                plot_bgcolor="#0c1022",
                font=dict(color="white"),
                margin=dict(l=0, r=0, t=20, b=10),
                showlegend=False,
                annotations=[dict(
                    text=f"<b>{tmp_pazar.iloc[0]['pazaryeri']}</b><br>{tmp_pazar.iloc[0]['oran']:.0f}%",
                    x=0.5, y=0.5, showarrow=False, font=dict(size=14)
                )]
            )
        else:
            fig_right = go.Figure()

    # Ne tür bir metrik? adet mi ₺ mi?
    is_tutar = any(x in label.lower() for x in ["kâr", "komisyon", "ciro", "kargo"])

    if is_tutar:
        if label == "Toplam Ciro":
            value_col = "satir_fiyat"
        elif label == "Net Kâr":
            value_col = "kar"
        elif label == "Komisyon":
            value_col = "satir_komisyon"
        elif label == "Kargo":
            value_col = "satir_kargo_fiyat"
        else:
            value_col = None
    else:
        value_col = None

    # GRAFİK 1 – MAĞAZA BAZLI
    if is_tutar and value_col:
        df_magaza = df_data.groupby("magaza_normalized")[value_col].sum().reset_index().sort_values(value_col, ascending=False)
        fig_top = px.bar(df_magaza, x=value_col, y="magaza_normalized", orientation="h", color_discrete_sequence=["#62caff"])
    else:
        df_magaza = df_data.groupby("magaza_normalized").size().reset_index(name="adet").sort_values("adet", ascending=False)
        fig_top = px.bar(df_magaza, x="adet", y="magaza_normalized", orientation="h", color_discrete_sequence=["#62caff"])

    fig_top.update_layout(
        height=240,
        paper_bgcolor="#0c1022", plot_bgcolor="#0c1022",
        font=dict(color="white"), margin=dict(l=0, r=0, t=20, b=10)
    )


    # GRAFİK 2 – PAZARYERİ BAZLI
    if is_tutar and value_col:
        df_pazar = (
            df_data.groupby("pazaryeri")[value_col]
            .sum()
            .reset_index()
            .rename(columns={value_col: "oran"})
        )
        total = df_pazar["oran"].sum()
        if total > 0:
            df_pazar["oran"] = df_pazar["oran"] / total * 100  # normalize et
    else:
        df_pazar = (
            df_data["pazaryeri"]
            .value_counts(normalize=True)
            .rename("oran")
            .reset_index()
            .rename(columns={"index": "pazaryeri"})
        )
        df_pazar["oran"] *= 100

    if df_pazar.empty:
        fig_bottom = go.Figure()
    else:
        fig_bottom = px.pie(df_pazar, names="pazaryeri", values="oran", hole=0.6,
                            color_discrete_sequence=["#00ffc3", "#00b2ff", "#1e90ff", "#4bc0c0"])
        max_row = df_pazar.iloc[0]
        fig_bottom.update_layout(
            height=220,
            paper_bgcolor="#0c1022", plot_bgcolor="#0c1022",
            font=dict(color="white"), margin=dict(l=0, r=0, t=20, b=10),
            showlegend=False,
            annotations=[dict(text=f"<b>{max_row['pazaryeri']}</b><br>{max_row['oran']:.0f}%",
                              x=0.5, y=0.5, showarrow=False, font=dict(size=14))]
        )

    # GRAFİKLERİ ÇİZ
    with st.container():
        st.plotly_chart(fig_top, use_container_width=True, key=f"top_{label}")
        if fig_bottom.data:
            st.plotly_chart(fig_bottom, use_container_width=True, key=f"bottom_{label}")


# ───────── Gauge + Expander Döngüsü ─────────
global_max       = max(m["value"] for m in metric_cards if any(x in m["label"].lower()
                               for x in ["kâr", "komisyon", "ciro", "kargo"]))
global_max_adet  = max(m["value"] for m in metric_cards if not any(x in m["label"].lower()
                               for x in ["kâr", "komisyon", "ciro", "kargo"]))

# ───────── Gauge + Expander Döngüsü (yeni düzen) ─────────
# her satır 4 metrik: (gauge, detay) × 4  →   toplam 8 sütun
rows = [metric_cards[:4], metric_cards[4:]]


for row in rows:
    # Her gauge + detay için iki sütun: solda gauge, sağda detay
    cols = st.columns([1, 2, 1, 2, 1, 2, 1, 2], gap="small")

    for i, metric in enumerate(row):
        col_left = cols[i * 2]      # Gauge grafik
        col_right = cols[i * 2 + 1] # Detay grafikler

        with col_left:
            st.plotly_chart(
                plot_gauge_gradient(
                    metric["value"], metric["label"],
                    base_colors, global_max,
                    adet_max=global_max_adet
                ),
                use_container_width=True,
                key=f"gauge_{metric['label']}"
            )

            # Butonla detay aç/kapat
            if st.button(f"🔍 Detay Göster", key=f"btn_{metric['label']}"):
                if st.session_state.get("aktif_metrik") == metric["label"]:
                    st.session_state["aktif_metrik"] = None
                else:
                    st.session_state["aktif_metrik"] = metric["label"]

        with col_right:
            if st.session_state.get("aktif_metrik") == metric["label"]:
                draw_metric_detail_v2(df_filtered, metric["label"], iade_df)




# -------------------- HARİTALARI YAN YANA VE ZOOM KAPALI --------------------
st.title("🌍 İl Bazında Ciro ve Kâr Dağılımı")

metric = st.radio(
    "Harita türünü seçin:",
    ["Ciro", "Kâr"],
    horizontal=True
)

# Seçime göre kolon adı ve renk skalası
if metric == "Ciro":
    color_col   = "Toplam Ciro"   # il_ozet’teki ciro sütunu
    color_scale = "Blues"
else:
    color_col   = "Net Kâr"       # il_ozet’teki kâr sütunu
    color_scale = "Greens"

# --------------------------------------------------------
# PLOTLY CHOROPLETH HARİTA
# --------------------------------------------------------
# "Sipariş" yoksa sözlükten çıkar
hover_dict = {
    "Toplam Ciro": ":,.0f ₺",
    "Net Kâr":     ":,.0f ₺",
    # "Sipariş":   ":,.0f adet",   # ← kolon henüz yok
}
fig = px.choropleth(
    il_ozet,
    geojson=turkiye_geojson,
    featureidkey="properties.name",
    locations="il",
    color=color_col,
    color_continuous_scale=color_scale,
    hover_name="il",
    hover_data=hover_dict,
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    dragmode=False,
    paper_bgcolor="rgba(0,0,0,0)",
    geo=dict(
        bgcolor="rgba(0,0,0,0)",
        projection_scale=9,
        center={"lat": 38.9, "lon": 35.1},
    ),
    coloraxis_colorbar=dict(
        title="₺",
        len=0.75,
        thickness=10,
        outlinewidth=0,
    ),
)

# --------------------------------------------------------
# HARİTAYI GÖSTER
# --------------------------------------------------------
st.plotly_chart(fig, use_container_width=True)

# 📊 Mağaza - Pazaryeri Özeti
# st.markdown("### 🧾 Mağaza & Pazaryeri Satış Özeti")

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


# 4. Stil ve render
# Küçültülmüş multiselect kutusu için stil ekleyelim
st.markdown("""
<style>
    /* Mağaza seçim kutusu genişliğini küçült */
    div[data-baseweb="select"] > div {
        max-width: 300px;
    }

    /* Pivot tablonun kapsayıcısı yatay scroll'u kaldır */
    div[data-testid="stDataFrame"] > div {
        overflow-x: hidden !important;
    }

    /* Tablo hücrelerini sıkıştır, satırda taşmayı engelle */
    table {
        table-layout: fixed !important;
        width: 100% !important;
        word-wrap: break-word !important;
        white-space: normal !important;
    }

    th, td {
        padding: 4px 8px !important;
        text-align: center !important;
        vertical-align: middle !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Sayfa genel scroll davranışını engelle */
html, body {
    overflow-y: hidden !important;
    height: 100% !important;
}

/* DataFrame bileşeninin scroll yapmasını engelle */
div[data-testid="stDataFrame"] {
    max-height: none !important;
    overflow: hidden !important;
}

/* İç kapsayıcılar da scroll yapmasın */
div[data-testid="stDataFrame"] > div {
    overflow: hidden !important;
    max-height: none !important;
}

/* Hücre ve tablo düzeni */
table {
    table-layout: fixed !important;
    width: 100% !important;
    word-wrap: break-word !important;
}
th, td {
    padding: 4px 8px !important;
    font-size: 14px !important;
}
</style>
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

# st.markdown("### 🏷️ Pazaryerine Göre Ciro, Kâr, Komisyon, Kargo")
#
# col12, col13 = st.columns(2)
#
# with col12:
#     st.subheader("💰 Ciro ve Kâr")
#
#     fig_ciro = px.bar(
#         grup,
#         x="pazaryeri",
#         y="Toplam Ciro",
#         title="Toplam Ciro",
#         text_auto=".2s",
#         labels={"pazaryeri": "Pazaryeri", "Toplam Ciro": "₺"}
#     )
#     fig_ciro.update_layout(dragmode=False)  # 👈 Zoom ve pan kapalı
#     st.plotly_chart(fig_ciro, use_container_width=True)
#
#     fig_kar = px.bar(
#         grup,
#         x="pazaryeri",
#         y="Net Kâr",
#         title="Net Kâr",
#         text_auto=".2s",
#         labels={"pazaryeri": "Pazaryeri", "Net Kâr": "₺"}
#     )
#     fig_kar.update_layout(dragmode=False)
#     st.plotly_chart(fig_kar, use_container_width=True)
#
# with col13:
#     st.subheader("📦 Kargo & Komisyon")
#
#     fig_kargo = px.bar(
#         grup,
#         x="pazaryeri",
#         y="Kargo Tutarı",
#         title="Kargo Tutarı",
#         text_auto=".2s",
#         labels={"pazaryeri": "Pazaryeri", "Kargo Tutarı": "₺"}
#     )
#     fig_kargo.update_layout(dragmode=False)
#     st.plotly_chart(fig_kargo, use_container_width=True)
#
#     fig_komisyon = px.bar(
#         grup,
#         x="pazaryeri",
#         y="Komisyon Tutarı",
#         title="Komisyon Tutarı",
#         text_auto=".2s",
#         labels={"pazaryeri": "Pazaryeri", "Komisyon Tutarı": "₺"}
#     )
#     fig_komisyon.update_layout(dragmode=False)
#     st.plotly_chart(fig_komisyon, use_container_width=True)

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

if "Stok" in urunler_df.columns:
    urunler_df["stok"] = urunler_df["Stok"].astype(str).str.replace(",", ".").str.strip()
    urunler_df["stok"] = pd.to_numeric(urunler_df["stok"], errors="coerce").fillna(0)

    stokta_olmayan_sayi = (urunler_df["stok"] <= 0).sum()
    kritik_stok_sayi = (urunler_df["stok"] <= 1).sum()
else:
    # st.warning("⚠️ 'Stok' kolonu bulunamadı, stok kontrolü atlandı.")
    stokta_olmayan_sayi = 0
    kritik_stok_sayi = 0

# 🎯 Stok durumu metriklerini renkli yuvarlak gösterge ile göster
st.markdown("### 📦 Stok Durumu Özeti")

stok_colors = ("#ff6b6b", "#ffa502")  # Kırmızıdan turuncuya geçiş
stok_max = max(stokta_olmayan_sayi, kritik_stok_sayi, 20)

col_stok1, col_stok2 = st.columns(2)
with col_stok1:
    st.plotly_chart(
        plot_gauge_gradient(stokta_olmayan_sayi, "🛑 Stokta Yok", stok_colors, stok_max, adet_max=stok_max),
        use_container_width=True
    )
with col_stok2:
    st.plotly_chart(
        plot_gauge_gradient(kritik_stok_sayi, "⚠️ Kritik Stok (<=1)", stok_colors, stok_max, adet_max=stok_max),
        use_container_width=True
    )
