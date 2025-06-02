import streamlit as st
import pandas as pd
import datetime
import unicodedata
import json
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

# label.css-1w0j46c, label.css-1y4p8pa { 
#     font-size: 15px !important;
#     color: #ecf0f1 !important;
#     padding-left: 8px;
# }
.st-emotion-cache-tj3uvl {
    padding: 0px calc(2px + 1rem) 19rem;
    margin-top: -26%;
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
# /* Sidebar başlık ve metinler */
# section[data-testid="stSidebar"] .css-1v0mbdj,
# section[data-testid="stSidebar"] .css-10trblm,
# section[data-testid="stSidebar"] h1,
# section[data-testid="stSidebar"] h2,
# section[data-testid="stSidebar"] h3,
# section[data-testid="stSidebar"] h4,
# section[data-testid="stSidebar"] label,
# section[data-testid="stSidebar"] span {
#     color: #f0f0f0 !important;
# }

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
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=220,
        width=220,
        paper_bgcolor="#0c1022",
        annotations=[dict(
            text=f'<b>{formatted_value}</b><br><span style="font-size:13px; color:#aaa">{label}</span>',
            x=0.5, y=0.5, font_size=16, showarrow=False
        )]
    )
    return fig
def metrik_aciklayici_grafik(metric_label, df):
    import plotly.express as px
    import plotly.graph_objects as go

    if metric_label in ["Toplam Sipariş", "Aktif Sipariş"]:
        veri = df["magaza_normalized"].value_counts().reset_index()
        veri.columns = ["Mağaza", "Adet"]
        fig = px.bar(veri, x="Adet", y="Mağaza", orientation="h", text="Adet",
                     color_discrete_sequence=["#00b2ff"])
        fig.update_layout(title="Mağaza Bazlı Sipariş", height=200,
                          paper_bgcolor="#0c1022", plot_bgcolor="#0c1022",
                          font=dict(color="white"), margin=dict(t=20, l=0, r=0, b=0))
        return fig

    elif metric_label == "İade":
        iade_veri = df[df["kar"] == 0]  # çünkü iade olanlarda kar sıfırlanmıştı
        veri = iade_veri["magaza_normalized"].value_counts().reset_index()
        veri.columns = ["Mağaza", "İade Adedi"]
        fig = px.bar(veri, x="İade Adedi", y="Mağaza", orientation="h", text="İade Adedi",
                     color_discrete_sequence=["#ff7675"])
        fig.update_layout(title="Mağaza Bazlı İade", height=200,
                          paper_bgcolor="#0c1022", font=dict(color="white"))
        return fig

    elif metric_label == "İptal":
        veri = df[df["siparis_satir_durumu"].str.lower() == "iptal"]["magaza_normalized"].value_counts().reset_index()
        veri.columns = ["Mağaza", "İptal Adedi"]
        fig = px.bar(veri, x="İptal Adedi", y="Mağaza", orientation="h", text="İptal Adedi",
                     color_discrete_sequence=["#d63031"])
        fig.update_layout(title="Mağaza Bazlı İptal", height=200,
                          paper_bgcolor="#0c1022", font=dict(color="white"))
        return fig

    elif metric_label == "Toplam Ciro":
        veri = df.groupby("pazaryeri")["satir_fiyat"].sum().reset_index()
        fig = px.pie(veri, names="pazaryeri", values="satir_fiyat", hole=0.5)
        fig.update_layout(title="Pazaryeri Bazlı Ciro", height=200,
                          paper_bgcolor="#0c1022", font=dict(color="white"))
        return fig

    elif metric_label == "Net Kâr":
        veri = df.groupby("magaza_normalized")["kar"].sum().reset_index()
        fig = px.bar(veri, x="kar", y="magaza_normalized", orientation="h", text="kar",
                     color_discrete_sequence=["#10ac84"])
        fig.update_layout(title="Mağaza Bazlı Kâr", height=200,
                          paper_bgcolor="#0c1022", font=dict(color="white"))
        return fig

    elif metric_label == "Komisyon":
        veri = df.groupby("pazaryeri")["satir_komisyon"].sum().reset_index()
        fig = px.pie(veri, names="pazaryeri", values="satir_komisyon", hole=0.4)
        fig.update_layout(title="Komisyon Dağılımı", height=200,
                          paper_bgcolor="#0c1022", font=dict(color="white"))
        return fig

    elif metric_label == "Kargo":
        veri = df.groupby("magaza_normalized")["satir_kargo_fiyat"].sum().reset_index()
        fig = px.pie(veri, names="magaza_normalized", values="satir_kargo_fiyat", hole=0.4)
        fig.update_layout(title="Kargo Dağılımı", height=200,
                          paper_bgcolor="#0c1022", font=dict(color="white"))
        return fig

    return None

@st.cache_data(show_spinner=False)
def cached_plot_gauge_gradient(value, label, base_colors, global_max, adet_max=25, total_slices=30):
    return plot_gauge_gradient(value, label, base_colors, global_max, adet_max, total_slices)

df = pd.read_excel("Siparisler.xlsx")
df["siparis_tarihi"] = pd.to_datetime(df["Sip. Tarihi"], errors="coerce")
df.columns = [c.strip() for c in df.columns]  # boşlukları temizle
df.rename(columns={
    "Mağaza": "magaza",
    "Pazaryeri": "pazaryeri",
    "Sipariş Satır Durumu": "siparis_satir_durumu"
}, inplace=True)

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

# Verilere manuel veriyi de ekle
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
# magazalar = ["sporsuit", "latte", "depoba", "ilyaki", "aida home", "perakende"]

# -------------------- FİLTRELER --------------------
# -------------------- SIDEBAR FİLTRELERİ (DÜZENLİ BLOKLAR) --------------------

st.sidebar.title("Dashboard")
with st.sidebar:
    st.markdown("## 📊 Filtreleme Paneli")

    # ---- TARİH FİLTRESİ ----
    st.markdown("### 📅 Tarih Filtresi")
    filtre_tipi = st.radio("Filtre Tipi Seç", ["Tarih Aralığı", "Dönem Bazlı"])
    # Mağaza normalize kolonu, pivot için gerekli
    df["magaza_normalized"] = df["magaza"].apply(normalize_magaza)

    if filtre_tipi == "Tarih Aralığı":
        tarih_aralik = st.date_input(
            "Tarih Aralığı Seç",
            [df["siparis_tarihi"].min().date(), df["siparis_tarihi"].max().date()]
        )
        # Kullanıcı hiç seçim yapmadıysa veya yalnızca 1 tarih girdiyse
        if not tarih_aralik or len(tarih_aralik) != 2:
            st.markdown("---")
            st.error("📅 Lütfen **başlangıç ve bitiş tarihini** seçiniz.")
            st.stop()
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

# MAĞAZA / PAZARYERİ FİLTRESİ
if "pazaryeri" not in df_filtered.columns:
    df_filtered["pazaryeri"] = df["pazaryeri"]
df_filtered = df_filtered[
    (df_filtered["magaza_normalized"].isin(secilen_magazalar)) &
    (df_filtered["pazaryeri"].isin(secilen_pazaryerleri))
    ]
# Normalize edilmiş mağaza sütununu tekrar uygula (gerekirse)
df["magaza_normalized"] = df["magaza"].apply(normalize_magaza)

# Sipariş Türleri
toplam_siparis = len(df_filtered)
iptal_sayisi = df_filtered[df_filtered["siparis_satir_durumu"].str.lower() == "iptal"].shape[0]
iade_sayisi = iade_df.shape[0]
aktif_siparis = toplam_siparis - iptal_sayisi - iade_sayisi

# Temel Sipariş Göstergeleri
st.markdown("### 📦 Sipariş ve Satış Özeti")
# 🎨 Renk paleti
# 🎨 Renk geçişi tanımı (mavi → yeşil)
base_colors = ("#00b2ff", "#00ffb3")

metrics = [
    {"label": "Toplam Sipariş", "value": toplam_siparis},
    {"label": "Aktif Sipariş", "value": aktif_siparis},
    {"label": "İade", "value": iade_sayisi},
    {"label": "İptal", "value": iptal_sayisi},
    {"label": "Toplam Ciro", "value": df_filtered["satir_fiyat"].sum()},
    {"label": "Net Kâr", "value": df_filtered["kar"].sum()},
    {"label": "Komisyon", "value": df_filtered["satir_komisyon"].sum()},
    {"label": "Kargo", "value": df_filtered["satir_kargo_fiyat"].sum()}
]

if metrics:
    global_max = max(m["value"] for m in metrics if any(x in m["label"].lower() for x in ["kâr", "komisyon", "ciro", "kargo", "maliyet", "tutar"]))
    global_max_adet = max((m["value"] for m in metrics if not any(x in m["label"].lower() for x in ["kâr", "komisyon", "ciro", "kargo", "maliyet", "tutar"])), default=25)

    for i in range(0, len(metrics), 4):
        cols = st.columns(4)
        for j, col in enumerate(cols):
            if i + j < len(metrics):
                metric = metrics[i + j]
                label = metric["label"]
                with col:
                    st.plotly_chart(
                        plot_gauge_gradient(metric["value"], label, base_colors, global_max, adet_max=global_max_adet),
                        use_container_width=True
                    )

                    # Her metrik için açıklayıcı grafik ekle
                    fig_explain = metrik_aciklayici_grafik(label, df_filtered)
                    if fig_explain:
                        st.plotly_chart(fig_explain, use_container_width=True, key=f"explain_{label}")

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
        dragmode=False,
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            projection_scale=9,
            center={"lat": 39.0, "lon": 35.0}
        ),
        coloraxis_colorbar=dict(
            thickness=10,
            len=0.6,
            title="₺"
        )
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
        dragmode=False,
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            projection_scale=9,
            center={"lat": 39.0, "lon": 35.0}
        ),
        coloraxis_colorbar=dict(
            thickness=10,
            len=0.6,
            title="₺"
        )
    )

    st.plotly_chart(fig_kar, use_container_width=True)

# Mağaza - Pazaryeri Özeti
# st.markdown("### 🧾 Mağaza & Pazaryeri Satış Özeti")

# Tüm mağazaların sabit listesi (veri olmasa bile görünsün)
tum_magaza_listesi = ["Sporsuit", "LATTE", "Depoba", "İLYAKİ", "AIDA HOME"]
tum_magazalar = [m.strip().lower().replace("ı", "i").capitalize() for m in tum_magaza_listesi]

# Tüm pazaryerlerini veriden al
# df["magaza_normalized"] = df["magaza"].astype(str).str.strip().str.lower().replace("ı", "i").str.capitalize()
df["pazaryeri"] = df["pazaryeri"].astype(str).str.strip()
tum_pazaryerleri = sorted(df["pazaryeri"].unique())

# Pazaryeri ve metrik yapısı
sabit_pazaryerleri = ["Amazon", "Trendyol", "PrestaShop", "Hepsiburada", "N11", "Perakende"]
metrikler = ["Satış", "Gider", "Kar"]
magazalar = ["sporsuit", "latte", "depoba", "ilyaki", "aida home"]

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

# Stok durumu metriklerini renkli yuvarlak gösterge ile göster
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
