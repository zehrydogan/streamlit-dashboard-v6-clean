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
    margin-top: -20%;
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


def normalize_il_name(il_adi):
    if pd.isnull(il_adi):
        return "Bilinmiyor"
    il_adi = str(il_adi).strip().title()

    il_mapping = {
        "Afyonkarahisar": "Afyon",
        "K.Maras": "Kahramanmaraş",
        "K.Maraş": "Kahramanmaraş",
        "Maras": "Kahramanmaraş",
        "Maraş": "Kahramanmaraş",
        "Istanbul": "İstanbul",
        "Izmir": "İzmir",
        "Sanliurfa": "Şanlıurfa",
        "Usak": "Uşak"
    }
    return il_mapping.get(il_adi, il_adi)


def interpolate_colors(start_hex, end_hex, n):
    if n <= 0:
        return []
    start_rgb = np.array(to_rgb(start_hex))
    end_rgb = np.array(to_rgb(end_hex))
    return [f'rgb({int(r*255)}, {int(g*255)}, {int(b*255)})'
            for r, g, b in np.linspace(start_rgb, end_rgb, n)]

# plot_gauge_gradient fonksiyonunda değişiklik (yaklaşık satır 250)
def plot_gauge_gradient(value, label, base_colors, global_max, adet_max=25, total_slices=50):
    is_tutar = any(x in label.lower() for x in ["kâr", "komisyon", "ciro", "kargo"])
    max_val = global_max if is_tutar else min(adet_max, global_max * 1.1)
    percentage = (value / max_val) * 100 if max_val != 0 else 0
    filled_slices = max(0, int((percentage / 100) * total_slices))
    empty_slices = total_slices - filled_slices
    gradient_colors = interpolate_colors(base_colors[0], base_colors[1], filled_slices)
    pie_colors = gradient_colors + ["#2c3e50"] * empty_slices

    # YENİ FORMATLAMA (Türkçe para formatı)
    if is_tutar:
        # Binlik ayraç: nokta, ondalık: virgül, 2 basamak
        formatted_value = "{:,.2f} ₺".format(value).replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        # Adetler için sadece binlik ayraç nokta
        formatted_value = "{:,} adet".format(int(value)).replace(",", ".")

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

@st.cache_data(show_spinner=False)
def cached_plot_gauge_gradient(value, label, base_colors, global_max, adet_max=25, total_slices=30):
    return plot_gauge_gradient(value, label, base_colors, global_max, adet_max, total_slices)

df = pd.read_excel("Temmuz_Siparisler.xlsx")
df["siparis_tarihi"] = pd.to_datetime(df["Sip. Tarihi"], format="%d.%m.%Y %H:%M", errors="coerce")
# ✅ ŞU SATIRI EKLE (manuel düzeltme)

df.columns = [
    unicodedata.normalize("NFKD", c)
    .encode("ascii", "ignore").decode("utf-8")
    .strip().lower()
    .replace(" ", "_").replace("-", "_")
    for c in df.columns
]
# ✅ İl sütununu normalize et
df["fatura_il"] = df["fatura___il"].apply(normalize_il_name)



df.rename(columns={"siparis_satr_durumu": "siparis_satir_durumu"}, inplace=True)
# Sütun isimlerini normalize et – Türkçe karakterleri düzelt, küçük harfe çevir


# df.columns = [c.strip() for c in df.columns]
# df.rename(columns={"Mağaza": "magaza"}, inplace=True)
with open("turkiye_il_sinirlar.json", "r", encoding="utf-8") as f:
    turkiye_geojson = json.load(f)

# Mağaza normalize et
df["magaza_normalized"] = df["magaza"].apply(normalize_magaza)


# -------------------- İADELER --------------------
# Sütun isimlerini normalize edelim
iade_df = pd.read_excel("Temmuz_Iadeler.xlsx")


iade_df.columns = [
    unicodedata.normalize("NFKD", c)
    .encode("ascii", "ignore").decode("utf-8")
    .strip().lower()
    .replace(" ", "_").replace("-", "_")
    for c in iade_df.columns
]

# Sadece "Onaylandı" olan iadeleri al
iade_df = iade_df[iade_df["iade_satr_durumu"].astype(str).str.strip().str.lower() == "onaylandı"]
iade_df["siparis_tarihi"] = pd.to_datetime(iade_df["iade_tarihi"], format="%d.%m.%Y %H:%M", errors="coerce").dt.date




iade_df["key"] = iade_df["siparis_no"].astype(str) + "|" + iade_df["stok_kodu"].astype(str)
df["key"] = df["siparis_no"].astype(str) + "|" + df["stok_kodu"].astype(str)



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

    tum_pazaryerleri = ["Amazon", "Trendyol", "PrestaShop", "HepsiBurada", "N11", "PraPazar"]
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

# Tarih Filtresi
if filtre_tipi == "Tarih Aralığı":
    if not tarih_aralik or len(tarih_aralik) < 2:
        st.warning("📅 Lütfen geçerli bir tarih aralığı seçiniz.")
        st.stop()
    else:
        baslangic, bitis = tarih_aralik
    df_filtered = df[
        (df["siparis_tarihi"].dt.date >= baslangic) &
        (df["siparis_tarihi"].dt.date <= bitis)
    ]
    df_filtered = df_filtered[[
        "siparis_no", "stok_kodu", "satr_fiyat", "kar", "fatura_il",
        "siparis_tarihi", "magaza_normalized", "pazaryeri",
        "satr_komisyon", "satr_kargo_fiyat", "siparis_satir_durumu",
        "key"
    ]]

    # Düzeltilmiş hali (filtrelenmiş veriye göre iadeler):
    iade_df = iade_df[iade_df["key"].isin(df_filtered["key"])]  # Sadece filtreli siparişlerdeki iadeler
    iade_sayisi = len(iade_df)

else:
    donem = f"{secilen_yil}-{aylar[ay_isimleri.index(secilen_ay)]:02d}"
    df_filtered = df[df["siparis_tarihi"].dt.strftime("%Y-%m") == donem]
    df_filtered = df_filtered[[
        "siparis_no", "stok_kodu", "satr_fiyat", "kar", "fatura_il",
        "siparis_tarihi", "magaza_normalized", "pazaryeri",
        "satr_komisyon", "satr_kargo_fiyat", "siparis_satir_durumu",
        "key"
    ]]

    iade_df = iade_df[
        iade_df["siparis_tarihi"].apply(lambda d: d.strftime("%Y-%m") == donem if pd.notnull(d) else False)
    ]

df_filtered["fatura_il"] = df_filtered["fatura_il"]  # test

# Sayısal kolonları düzelt
sayisal_kolonlar = [
    "satr_fiyat",
    "urun_toplam_maliyet",
    "satr_komisyon",
    "satr_kargo_fiyat"
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

for kolon in sayisal_kolonlar:
    df_filtered = temizle_sayisal_kolon(df_filtered, kolon)

# 🔧 Ham veri için de kargo sütununu dönüştür
df = temizle_sayisal_kolon(df, "satr_kargo_fiyat")


# Kar hesapla
df_filtered["kar"] = (
    df_filtered["satr_fiyat"]
    - df_filtered["urun_toplam_maliyet"]
    - df_filtered["satr_komisyon"]
    - df_filtered["satr_kargo_fiyat"]
)


df_filtered["satr_fiyat"] = pd.to_numeric(df_filtered["satr_fiyat"], errors="coerce").fillna(0)
df_filtered["kar"] = pd.to_numeric(df_filtered["kar"], errors="coerce").fillna(0)
df_filtered["urun_toplam_maliyet"] = pd.to_numeric(df_filtered["urun_toplam_maliyet"], errors="coerce").fillna(0)

# 4. İl bazında özet veriyi oluştur
il_ozet = df_filtered.groupby("fatura_il").agg({
    "satr_fiyat": "sum",
    "kar": "sum"
}).reset_index().rename(columns={
    "fatura_il": "il",
    "satr_fiyat": "Toplam Ciro",
    "kar": "Net Kâr"
})


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
# 🔢 Sipariş Türleri
toplam_siparis = df_filtered["siparis_no"].astype(str).count()

# İptal sayısı (filtreli veri üzerinden)
# YENİ KODLAR (EKLEYİN)
# Ham veriden iptal siparişleri filtrele
# İPTAL SİPARİŞLERİ HESAPLA
# Ham veriden iptalleri hesapla (df_filtered yerine df kullanın)
# 'siparis_satir_durumu' sütununu kullanın
# 'siparis_satir_durumu' sütununu kullanın
iptal_df = df_filtered[
    df_filtered["siparis_satir_durumu"].astype(str)
    .str.strip()
    .str.lower()
    .str.contains("iptal|i̇ptal", regex=True, na=False)
]
iptal_sayisi = len(iptal_df)
iade_sayisi = len(iade_df)

# Aktif sipariş: İade DEĞİL ve İptal DEĞİL olanlar
# Aktif sipariş = Filtrelenmiş verideki satır sayısı (zaten iptaller filtrelenmiş)

# Aktif siparişleri doğrudan filtreleyerek hesapla
# Yöntem 1: Toplam - (İptal + İade)
aktif_siparis  = toplam_siparis - iptal_sayisi - iade_sayisi

# Yöntem 2: Direkt filtreleme (durum = "aktif" VE iade/iptal değil)
aktif_df = df_filtered[
    (~df_filtered["key"].isin(iade_df["key"])) &
    (~df_filtered["key"].isin(iptal_df["key"])) &
    (df_filtered["siparis_satir_durumu"].str.lower().str.contains("aktif|tamamlandı", regex=True))
]

# 📦 Temel Sipariş Göstergeleri
st.markdown("### 📦 Sipariş ve Satış Özeti")
base_colors = ("#00b2ff", "#00ffb3")

# 3. METRİKLERİ GÜNCELLE (FİLTRELENMİŞ VERİYLE)
metric_cards = [
    {"label": "Toplam Sipariş", "value": df_filtered["siparis_no"].astype(str).count()},
    {"label": "Aktif Sipariş", "value": df_filtered["siparis_no"].astype(str).count() - iptal_sayisi - iade_sayisi},
    {"label": "İade", "value": iade_sayisi},
    {"label": "İptal", "value": iptal_sayisi},
    {"label": "Toplam Ciro", "value": df_filtered["satr_fiyat"].sum()},
    {"label": "Net Kâr", "value": df_filtered["kar"].sum()},
    {"label": "Komisyon", "value": df_filtered["satr_komisyon"].sum()},
    {"label": "Kargo", "value": df_filtered["satr_kargo_fiyat"].sum()},
]
# İPTAL DETAYLARINI GÖSTER

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
            value_col = "satr_fiyat"
        elif label == "Net Kâr":
            value_col = "kar"
        elif label == "Komisyon":
            value_col = "satr_komisyon"
        elif label == "Kargo":
            value_col = "satr_kargo_fiyat"
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
global_max = max([
    df_filtered["satr_fiyat"].sum(),
    df_filtered["kar"].sum(),
    df_filtered["satr_komisyon"].sum(),
    df_filtered["satr_kargo_fiyat"].sum()  # <-- Filtrelenmiş veri kullan
])
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

        label = metric["label"]
        value = metric["value"]

        # Eğer "Kargo" ise farklı maksimum kullan
        if label.lower() == "kargo":
            local_max = df["satr_kargo_fiyat"].sum() * 1.2  # %20 boşluk bırak
        else:
            local_max = global_max

        with col_left:
            st.plotly_chart(
                plot_gauge_gradient(
                    value, label,
                    base_colors, local_max,
                    adet_max=global_max_adet
                ),
                use_container_width=True,
                key=f"gauge_{label}"
            )

        #     if st.button(f"🔍 Detay Göster", key=f"btn_{label}"):
        #         if st.session_state.get("aktif_metrik") == label:
        #             st.session_state["aktif_metrik"] = None
        #         else:
        #             st.session_state["aktif_metrik"] = label
        #
        # with col_right:
        #     if st.session_state.get("aktif_metrik") == label:
        #         draw_metric_detail_v2(df_filtered, label, iade_df)

# -------------------- HARİTA KISMI --------------------
st.title("🌍 İl Bazında Ciro ve Kâr Dağılımı")

metric = st.radio(
    "Harita türünü seçin:",
    ["Ciro", "Kâr"],
    horizontal=True
)

# Filtrelenmiş veriden il özetini oluştur
il_ozet = df_filtered.groupby("fatura_il").agg({
    "satr_fiyat": "sum",
    "kar": "sum"
}).reset_index().rename(columns={
    "fatura_il": "il",
    "satr_fiyat": "Toplam Ciro",
    "kar": "Net Kâr"
})

# İl isimlerini standartlaştır
il_ozet["il"] = il_ozet["il"].apply(normalize_il_name)

# Seçime göre kolon adı ve renk skalası
if metric == "Ciro":
    color_col = "Toplam Ciro"
    color_scale = "Blues"
    hover_data = {
        "Toplam Ciro": True,
        "Net Kâr": False,
        "il": False
    }
else:
    color_col = "Net Kâr"
    color_scale = "Greens"
    hover_data = {
        "Toplam Ciro": False,
        "Net Kâr": True,
        "il": False
    }

# GeoJSON'daki tüm illeri al
geo_iller = [feature["properties"]["name"] for feature in turkiye_geojson["features"]]
# Eksik illeri bul ve 0 değerleriyle ekle
eksik_iller = list(set(geo_iller) - set(il_ozet["il"]))
eksik_df = pd.DataFrame({
    "il": eksik_iller,
    "Toplam Ciro": 0,
    "Net Kâr": 0
})
il_ozet = pd.concat([il_ozet, eksik_df], ignore_index=True)

# Formatlı sütunlar ekleyelim
il_ozet["Toplam Ciro Formatlı"] = il_ozet["Toplam Ciro"].apply(
    lambda x: f"{x:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", ".")
)
il_ozet["Net Kâr Formatlı"] = il_ozet["Net Kâr"].apply(
    lambda x: f"{x:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", ".")
)

if metric == "Ciro":
    hover_data = {
        "il": False,
        "Toplam Ciro Formatlı": True,
        "Net Kâr Formatlı": False,
        "Toplam Ciro": False,
        "Net Kâr": False
    }
else:
    hover_data = {
        "il": False,
        "Toplam Ciro Formatlı": False,
        "Net Kâr Formatlı": True,
        "Toplam Ciro": False,
        "Net Kâr": False
    }


# Harita oluşturma kısmını şu şekilde güncelleyin:
fig = px.choropleth(
    il_ozet,
    geojson=turkiye_geojson,
    locations="il",
    featureidkey="properties.name",
    color=color_col,
    color_continuous_scale=color_scale,
    hover_name="il",
    hover_data={
        "il": False,
        "Toplam Ciro": False,  # Ham veriyi gizle
        "Net Kâr": False,      # Ham veriyi gizle
        "Toplam Ciro Formatlı": True,  # Formatlı versiyonu göster
        "Net Kâr Formatlı": True       # Formatlı versiyonu göster
    },
    custom_data=["Toplam Ciro", "Net Kâr"],  # Hesaplamalar için ham veriyi sakla
    labels={
        "Toplam Ciro Formatlı": "Toplam Ciro",
        "Net Kâr Formatlı": "Net Kâr"
    }
)

# Hover template'i manuel olarak ayarla
fig.update_traces(
    hovertemplate="<b>%{location}</b><br>" +
    ("Toplam Ciro: %{customdata[0]:,.2f} ₺<extra></extra>" if metric == "Ciro" else
     "Net Kâr: %{customdata[1]:,.2f} ₺<extra></extra>")
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
st.plotly_chart(fig, use_container_width=True)
# -------------------- PİVOT TABLO --------------------
st.markdown("### 🏷️ Mağaza & Pazaryeri Satış Özeti")

# Create pivot table with the structure from your image
pivot_data = []

# Define the store and marketplace structure from your image
# store_structure = {
#     "AIDA HOME": ["PrestaShop", "Trendyol"],
#     "Depoba": ["Amazon", "Trendyol"],
#     "ILYAKİ": ["HepsiBurada", "Trendyol"],
#     "LATTE": ["Amazon", "Trendyol"],
#     "Sporsuit": ["Amazon", "PraPazar", "PrestaShop", "Trendyol"]
# }

# Dinamik olarak mevcut mağaza ve pazaryeri kombinasyonlarını al
filtered_stores = df_filtered["magaza_normalized"].unique()

pivot_data = []

for store in filtered_stores:
    store_df = df_filtered[df_filtered["magaza_normalized"] == store]
    filtered_marketplaces = store_df["pazaryeri"].unique()

    for i, marketplace in enumerate(filtered_marketplaces):
        filtered = store_df[store_df["pazaryeri"] == marketplace]
        komisyon = filtered["satr_komisyon"].sum()
        net_kar = filtered["kar"].sum()

        pivot_data.append({
            "Mağaza": store.upper() if i == 0 else "",
            "Pazaryeri": marketplace,
            "Komisyon": f"{komisyon:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", "."),
            "Net Kar": f"{net_kar:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", ".")
        })

    # Mağaza toplamı
    total_komisyon = store_df["satr_komisyon"].sum()
    total_net_kar = store_df["kar"].sum()

    pivot_data.append({
        "Mağaza": f"Toplam {store.upper()}",
        "Pazaryeri": "",
        "Komisyon": f"{total_komisyon:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", "."),
        "Net Kar": f"{total_net_kar:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", ".")
    })

grand_total_komisyon = df_filtered["satr_komisyon"].sum()
grand_total_net_kar = df_filtered["kar"].sum()
pivot_data.append({
    "Mağaza": "Genel Toplam",
    "Pazaryeri": "",
    "Komisyon": f"{grand_total_komisyon:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", "."),
    "Net Kar": f"{grand_total_net_kar:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", ".")
})

# Convert to DataFrame
pivot_df = pd.DataFrame(pivot_data)

# Display the pivot table with custom styling
# st.dataframe(
#     pivot_df,
#     use_container_width=True,
#     hide_index=True,
#     column_config={
#         "Mağaza": st.column_config.Column(width="medium"),
#         "Pazaryeri": st.column_config.Column(width="medium"),
#         "Komisyon": st.column_config.Column(width="medium"),
#         "Net Kar": st.column_config.Column(width="medium")
#     }
# )
# HTML tabloyu oluştur
pivot_html = pivot_df.to_html(index=False, escape=False, border=0, classes="custom-pivot-table")
st.markdown("""
<style>
.custom-pivot-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 15px;
    font-family: 'Segoe UI', sans-serif;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}

/* BAŞLIKLAR */
.custom-pivot-table th {
    background: linear-gradient(to right, #002f4b, #005c97);
    color: white;
    padding: 14px;
    font-weight: 700;
    font-size: 15px;
    text-align: center;
    border-bottom: 3px solid #00c3ff;
}

/* HÜCRELER */
.custom-pivot-table td {
    background-color: #0f1626;
    color: #ecf0f1;
    padding: 12px 10px;
    border-bottom: 1px solid #2f3640;
    font-size: 14px;
    text-align: center;
    transition: background-color 0.2s ease;
}

/* ALTERNATİF SATIR */
.custom-pivot-table tr:nth-child(even) td {
    background-color: #10192e;
}

/* HOVER */
.custom-pivot-table tr:hover td {
    background-color: #1d2d44;
}

/* ₺ SÜTUNLARI */
.custom-pivot-table td:nth-child(3),
.custom-pivot-table td:nth-child(4) {
    text-align: right;
    font-family: 'Courier New', monospace;
    font-variant-numeric: tabular-nums;
}

/* MAĞAZA SATIRI (ilk satırda) */
.custom-pivot-table td:first-child:not(:empty):not(:has(+ td:not(:empty))) {
    font-weight: bold;
    background-color: #1c3147;
    color: #00d2ff;
    font-size: 16px;
    text-align: left;
    border-left: 5px solid #00f0ff;
    border-top: 2px solid #00c3ff;
}

/* TOPLAM SATIRLAR */
.custom-pivot-table td:first-child:contains("Toplam") {
    background: linear-gradient(to right, #00334e, #002637);
    color: #7fdbff !important;
    font-weight: bold;
    font-size: 15px;
    text-align: left;
    border-left: 5px solid #00ffcc;
    box-shadow: inset 2px 0 0 #00ffcc;
}

/* GENEL TOPLAM */
.custom-pivot-table td:first-child:contains("Genel Toplam") {
    background-color: #ffe600 !important;
    color: #000000 !important;
    font-weight: 900;
    font-size: 16px;
    border-left: 6px solid #ff8800;
    text-align: left;
    box-shadow: inset 4px 0 0 #ff8800;
}

/* GENEL TOPLAM TÜM SATIR */
.custom-pivot-table tr td:first-child:contains("Genel Toplam") ~ td {
    background-color: #fff9c4 !important;
    color: #111 !important;
    font-weight: bold;
}

.custom-pivot-table tr td:empty {
    background-color: #0f1626;
}
</style>
""", unsafe_allow_html=True)



# HTML tabloyu göster
st.markdown(pivot_html, unsafe_allow_html=True)

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
sabit_pazaryerleri = ["Amazon", "Trendyol", "PrestaShop", "HepsiBurada", "N11", "Perakende"]
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
# GRAFİKLER

st.markdown("### 📈 Günlük Ciro & Net Kâr")

# Günlük veriyi hazırla
daily = df_filtered.groupby(df_filtered["siparis_tarihi"].dt.date).agg({
    "satr_fiyat": "sum",
    "kar": "sum"
}).rename(columns={"satr_fiyat": "Toplam Ciro", "kar": "Net Kâr"}).reset_index()

daily["Tarih"] = pd.to_datetime(daily["siparis_tarihi"])

# Uzun formata çevir
daily_melted = daily.melt(
    id_vars="Tarih",
    value_vars=["Toplam Ciro", "Net Kâr"],
    var_name="Gösterge",
    value_name="Tutar"
)

# Format the values properly for display
daily_melted["Tutar_Formatted"] = daily_melted["Tutar"].apply(lambda x: f"{x:,.2f} ₺")

# Altair grafik
chart = alt.Chart(daily_melted).mark_line(point=True).encode(
    x=alt.X("yearmonthdate(Tarih):T", title="Tarih", axis=alt.Axis(format="%d %b", labelAngle=0)),
    y=alt.Y("Tutar:Q", title="Tutar (₺)", axis=alt.Axis(format=",.0f")),
    color=alt.Color("Gösterge:N", title="Gösterge"),
    tooltip=[
        alt.Tooltip("yearmonthdate(Tarih):T", title="Tarih", format="%d %B %Y"),
        alt.Tooltip("Gösterge:N", title="Gösterge"),
        alt.Tooltip("Tutar_Formatted:N", title="Tutar")  # Use formatted value
    ]
).properties(
    height=400
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_legend(
    titleFontSize=13,
    labelFontSize=12,
    orient='bottom'
)

# Streamlit'te düzgün yerleşimle göster
st.altair_chart(chart, use_container_width=True)

# Pazaryerine göre gruplama
grup = df_filtered.groupby("pazaryeri").agg({
    "satr_fiyat": "sum",
    "kar": "sum",
    "satr_kargo_fiyat": "sum",
    "satr_komisyon": "sum"
}).reset_index().rename(columns={
    "satr_fiyat": "Toplam Ciro",
    "kar": "Net Kâr",
    "satr_kargo_fiyat": "Kargo Tutarı",
    "satr_komisyon": "Komisyon Tutarı"
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
# urunler_df = pd.read_excel("Urunler.xlsx")
# urunler_df.columns = [
#     c.strip().lower()
#     .replace(" ", "_")
#     .replace("-", "_")
#     .replace("ç", "c").replace("ş", "s").replace("ğ", "g")
#     .replace("ü", "u").replace("ı", "i").replace("ö", "o")
#     for c in urunler_df.columns
# ]
#
# if "Stok" in urunler_df.columns:
#     urunler_df["stok"] = urunler_df["Stok"].astype(str).str.replace(",", ".").str.strip()
#     urunler_df["stok"] = pd.to_numeric(urunler_df["stok"], errors="coerce").fillna(0)
#
#     stokta_olmayan_sayi = (urunler_df["stok"] <= 0).sum()
#     kritik_stok_sayi = (urunler_df["stok"] <= 1).sum()
# else:
#     # st.warning("⚠️ 'Stok' kolonu bulunamadı, stok kontrolü atlandı.")
#     stokta_olmayan_sayi = 0
#     kritik_stok_sayi = 0

# 🎯 Stok durumu metriklerini renkli yuvarlak gösterge ile göster
# st.markdown("### 📦 Stok Durumu Özeti")
#
# stok_colors = ("#ff6b6b", "#ffa502")  # Kırmızıdan turuncuya geçiş
# stok_max = max(stokta_olmayan_sayi, kritik_stok_sayi, 20)
#
# col_stok1, col_stok2 = st.columns(2)
# with col_stok1:
#     st.plotly_chart(
#         plot_gauge_gradient(stokta_olmayan_sayi, "🛑 Stokta Yok", stok_colors, stok_max, adet_max=stok_max),
#         use_container_width=True
#     )
# with col_stok2:
#     st.plotly_chart(
#         plot_gauge_gradient(kritik_stok_sayi, "⚠️ Kritik Stok (<=1)", stok_colors, stok_max, adet_max=stok_max),
#         use_container_width=True
#     )
