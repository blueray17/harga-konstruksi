import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Check Harga Konstruksi", layout="centered", page_icon="🏗️")

# ============================================================
# KONFIGURASI GOOGLE SHEET
# ============================================================
SHEET_ID = "1uuuZhUlzolwlxBx5lothgtBeEr4t5SuK"
GID = "0"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"


@st.cache_data(ttl=300)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception:
        # return pd.DataFrame()
        return pd.DataFrame({
            "kode": [
                "1. Tanah Uruk (tanah biasa)", "2. Pasir Pasang", "3. Pasir cor/beton",
                "4. Batu pondasi (batu gunung)", "5. Batu Bata Tanah Liat",
                "6. batako tidak berlubang", "7. Batu split 1-2 cm",
                "8. Kayu balok (kayu kelas II)", "9. Kayu balok (kayu kelas III)",
                "10. Kayu papan (kayu kelas II)",
            ],
            "Penghitungan": ["volume"] * 10,
            "Harga Bawah": [140000, 205000, 205000, 205000, 500000, 446000, 205000,
                             8680000, 4167000, 9375000],
            "Harga Atas": [205000, 379000, 393000, 294000, 781000, 595000, 315000,
                            9470000, 4687500, 11250000],
            "satuan": ["m"] * 10,
        })


def rupiah(nilai) -> str:
    return f"Rp {nilai:,.0f}".replace(",", ".")


def format_angka_id(nilai, max_desimal: int = 2) -> str:
    """Format angka gaya Indonesia: titik sebagai pemisah ribuan, koma sebagai pemisah desimal."""
    nilai = round(float(nilai), max_desimal)
    if nilai == int(nilai):
        formatted = f"{int(nilai):,}"
    else:
        formatted = f"{nilai:,.{max_desimal}f}".rstrip("0").rstrip(".")
    # tukar posisi separator: koma bawaan Python -> titik ribuan, titik bawaan -> koma desimal
    return formatted.replace(",", "§").replace(".", ",").replace("§", ".")


# ============================================================
# TEMA ORANGE - nuansa Sensus Ekonomi (kompak untuk mobile)
# ============================================================
ORANGE = "#F26522"
ORANGE_DARK = "#C64A0A"
ORANGE_MID = "#FF8A3D"
ORANGE_LIGHT = "#FFF3E8"
CREAM = "#FFFBF6"
TEXT_DARK = "#3A2A1E"

st.markdown(
    f"""
    <style>
        .stApp {{ background-color: {CREAM}; }}
        .block-container {{
            padding-top: 3rem;
            padding-bottom: 1rem;
            max-width: 680px;
        }}
        /* rapatkan jarak antar elemen agar kompak di mobile */
        div[data-testid="stVerticalBlock"] > div {{
            margin-bottom: 0.15rem;
        }}
        div[data-testid="element-container"] {{
            margin-bottom: 0.2rem !important;
        }}

        /* ---------- Header banner ---------- */
        .header-banner {{
            background: linear-gradient(120deg, {ORANGE} 0%, {ORANGE_MID} 60%, {ORANGE_DARK} 100%);
            border-radius: 16px;
            padding: 16px 18px;
            margin-bottom: 12px;
            box-shadow: 0 6px 16px rgba(242, 101, 34, 0.28);
            text-align: center;
        }}
        .header-title {{
            color: white;
            font-size: 22px;
            font-weight: 800;
            margin: 0;
        }}
        .header-sub {{
            color: {ORANGE_LIGHT};
            font-size: 12px;
            font-weight: 500;
            margin-top: 2px;
        }}

        .section-title {{
            color: {ORANGE_DARK};
            font-weight: 700;
            font-size: 14px;
            margin: 10px 0 4px 0;
        }}

        /* ---------- Labels & widgets ---------- */
        label {{
            color: {ORANGE_DARK} !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }}

        /* ---------- Selectbox: paksa terang di semua level & mode ---------- */
        div[data-testid="stSelectbox"] div[data-baseweb="select"],
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] div {{
            background-color: {ORANGE_LIGHT} !important;
            border-color: {ORANGE} !important;
        }}
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
            border: 1.5px solid {ORANGE} !important;
            border-radius: 10px !important;
            box-shadow: none !important;
        }}
        div[data-testid="stSelectbox"] * {{
            color: {TEXT_DARK} !important;
            fill: {TEXT_DARK} !important;
        }}
        /* panel opsi (popover terpisah dari DOM utama) */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] div,
        ul[role="listbox"] {{
            background-color: white !important;
        }}
        div[data-baseweb="popover"] li,
        ul[role="listbox"] li {{
            color: {TEXT_DARK} !important;
            background-color: white !important;
            font-weight: 500;
        }}
        div[data-baseweb="popover"] li:hover,
        ul[role="listbox"] li:hover {{
            background-color: {ORANGE_LIGHT} !important;
        }}

        input[type="number"] {{
            background-color: {ORANGE_LIGHT} !important;
            border: 1.5px solid {ORANGE} !important;
            border-radius: 10px !important;
            color: {TEXT_DARK} !important;
        }}

        .info-box {{
            background: linear-gradient(135deg, {ORANGE_LIGHT} 0%, white 100%);
            border: 1.5px solid {ORANGE};
            border-radius: 12px;
            padding: 10px 14px;
            margin: 4px 0;
        }}
        .info-label {{
            font-size: 13px;
            font-weight: 700;
            color: {ORANGE_DARK};
        }}
        .info-value {{
            font-size: 20px;
            font-weight: 800;
            color: {TEXT_DARK};
        }}
        .range-label {{
            font-size: 14px;
            font-weight: 700;
            color: {ORANGE_DARK};
            margin-bottom: 2px;
        }}
        .range-value {{
            font-size: 20px;
            font-weight: 800;
            color: {TEXT_DARK};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

df = load_data()

# ---------------- auto-select isi input angka saat diklik/fokus ----------------
components.html(
    """
    <script>
    try {
        const doc = window.parent.document;
        if (!doc.__autoSelectNumberAttached) {
            doc.addEventListener('focusin', function (e) {
                const el = e.target;
                if (el && el.tagName === 'INPUT' && el.type === 'number') {
                    el.select();
                }
            });
            doc.__autoSelectNumberAttached = true;
        }
    } catch (err) {}
    </script>
    """,
    height=0,
)

# ---------------- header ----------------
st.markdown(
    """
    <div class="header-banner">
        <div class="header-title">🏗️ Check Harga Konstruksi</div>
        <div class="header-sub">Pemantauan Harga Komoditas Bahan Bangunan - BPS Provinsi Lampung</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- pilih komoditas ----------------
st.markdown('<div class="section-title">📋 Pilih Jenis Komoditas</div>', unsafe_allow_html=True)
pilihan = st.selectbox(" ", df["kode"].tolist(), label_visibility="collapsed")

row = df[df["kode"] == pilihan].iloc[0]
batas_bawah = float(row["Harga Bawah"])
batas_atas = float(row["Harga Atas"])
satuan = str(row["satuan"]).strip() if "satuan" in row and pd.notna(row["satuan"]) else "m"
label_hitung = (
    str(row["Penghitungan"]).strip()
    if "Penghitungan" in row and pd.notna(row["Penghitungan"])
    else "Volume"
)

# ---------------- dimensi ----------------
st.markdown('<div class="section-title">📐 Ukuran / Dimensi</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    panjang = st.number_input(f"Panjang ({satuan})", min_value=0.0, value=0.0, step=0.1)
with c2:
    lebar = st.number_input(f"Lebar ({satuan})", min_value=0.0, value=0.0, step=0.1)
with c3:
    tinggi = st.number_input(f"Tinggi ({satuan})", min_value=0.0, value=0.0, step=0.1)

volume = panjang * lebar * tinggi

st.markdown(
    f"""<div class="info-box">
            <div class="info-label">📦 {label_hitung.capitalize()}</div>
            <div class="info-value">{format_angka_id(volume)} {satuan}</div>
        </div>""",
    unsafe_allow_html=True,
)

# ---------------- batas bawah / atas ----------------
b1, b2 = st.columns(2)
with b1:
    st.markdown(
        f"""<div class="info-box">
                <div class="range-label">⬇️ Batas Bawah</div>
                <div class="range-value">{rupiah(batas_bawah)}</div>
            </div>""",
        unsafe_allow_html=True,
    )
with b2:
    st.markdown(
        f"""<div class="info-box">
                <div class="range-label">⬆️ Batas Atas</div>
                <div class="range-value">{rupiah(batas_atas)}</div>
            </div>""",
        unsafe_allow_html=True,
    )

# ---------------- Total Harga (realtime, murni JS/HTML) ----------------
component_html = f"""
<div style="font-family: 'Source Sans Pro', sans-serif; padding-bottom:14px;">
    <div style="background-color:white; border:1px solid #FBD9BE; border-radius:12px;
                padding:12px 14px; box-shadow:0 3px 10px rgba(242,101,34,0.08); margin-top:6px;">
        <div style="color:{ORANGE_DARK}; font-weight:700; font-size:13px; margin-bottom:6px;">
            💰 Total Harga
        </div>
        <input id="totalHarga" type="text" inputmode="numeric" placeholder="0"
            style="width:100%; box-sizing:border-box; padding:9px 10px;
                   font-size:18px; border:1.5px solid {ORANGE}; border-radius:10px;
                   background-color:{ORANGE_LIGHT}; color:{TEXT_DARK}; outline:none;" />
    </div>

    <div style="margin-top:10px; background: linear-gradient(135deg, {ORANGE_LIGHT} 0%, white 100%);
                border:1.5px solid {ORANGE}; border-radius:12px; padding:10px 14px;
                box-shadow:0 3px 10px rgba(242,101,34,0.10);">
        <div style="font-size:13px; font-weight:700; color:{ORANGE_DARK};">📊 Nilai per Satuan ({satuan})</div>
        <div id="nilaiPerSatuan" style="font-size:20px; font-weight:800; color:{TEXT_DARK};">Rp 0</div>
    </div>

    <div id="warningBox" style="display:none; margin-top:8px; padding:12px; border-radius:10px;
         font-weight:700; font-size:14px; color:white;">
    </div>
</div>

<script>
    const volume = {volume};
    const batasBawah = {batas_bawah};
    const batasAtas = {batas_atas};

    const input = document.getElementById('totalHarga');
    const hasilEl = document.getElementById('nilaiPerSatuan');
    const warnEl = document.getElementById('warningBox');

    function formatRibuan(digits) {{
        if (!digits) return '';
        return parseInt(digits, 10).toLocaleString('id-ID');
    }}

    function formatRupiah(angka) {{
        return 'Rp ' + Math.round(angka).toLocaleString('id-ID');
    }}

    input.addEventListener('input', function () {{
        const digits = input.value.replace(/[^0-9]/g, '');
        input.value = formatRibuan(digits);

        const totalHarga = digits ? parseInt(digits, 10) : 0;
        const nilaiPerSatuan = (volume > 0) ? (totalHarga / volume) : 0;

        hasilEl.textContent = formatRupiah(nilaiPerSatuan);

        if (totalHarga > 0 && volume > 0) {{
            const nilaiFormatted = formatRibuan(String(Math.round(nilaiPerSatuan)));
            const inRange = nilaiPerSatuan >= batasBawah && nilaiPerSatuan <= batasAtas;

            warnEl.style.display = 'block';
            if (inRange) {{
                warnEl.style.backgroundColor = '#2E9E4F';
                warnEl.style.boxShadow = '0 4px 12px rgba(46,158,79,0.35)';
                warnEl.textContent = '✅ Harga Komoditas ' + nilaiFormatted +
                    ' Sesuai Dengan Rentang Harga';
            }} else {{
                warnEl.style.backgroundColor = '#D9432B';
                warnEl.style.boxShadow = '0 4px 12px rgba(217,67,43,0.35)';
                warnEl.textContent = '⚠️ Harga Komoditas ' + nilaiFormatted +
                    ' Tidak Sesuai Dengan Rentang Harga';
            }}
        }} else {{
            warnEl.style.display = 'none';
        }}
    }});
</script>
"""

components.html(component_html, height=260, scrolling=False)
