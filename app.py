# -*- coding: utf-8 -*-
"""KODE PROGRAM PROJECT CEK MB DYELOT.ipynb"""

import io
import re
import pandas as pd
import streamlit as st

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="MB-VANGUARD | Audit Data Manufacture Basic",
    page_icon="⚡",
    layout="wide",
)

# Custom Styling CSS - Tema Modern Dark Slate (Executive Dark Mode)
st.markdown(
    """
    <style>
    /* Global Dark Theme Styling */
    .stApp {
        background-color: #0B0F19;
        color: #F1F5F9;
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header Utama */
    .main-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 30px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.25rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        color: #00F2FE;
    }
    .main-header p {
        margin: 8px 0 0 0;
        font-size: 1.05rem;
        color: #94A3B8;
        font-weight: 400;
    }

    /* Kontras Kartu Metrik (Dark Mode Optimized) */
    div[data-testid="metric-container"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        border-color: #00F2FE;
    }
    div[data-testid="metric-container"] label {
        color: #94A3B8 !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #00F2FE !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }

    /* Tombol Aksi Utama (Button Eksekusi) */
    div.stButton > button {
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
        color: #0B0F19 !important;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
        transition: all 0.25s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #4FACFE 0%, #00F2FE 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
        color: #0B0F19 !important;
    }

    /* Tombol Download (Kontras teks terang & jelas) */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #334155 100%, #1E293B 0%);
        color: #00F2FE !important;
        font-weight: 600;
        border: 1px solid #475569;
        border-radius: 10px;
        padding: 12px 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.25s ease;
        width: 100%;
    }
    div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, #475569 100%, #334155 0%);
        color: #FFFFFF !important;
        border-color: #00F2FE;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 242, 254, 0.2);
    }
    div.stDownloadButton > button p, 
    div.stDownloadButton > button span {
        color: inherit !important;
    }

    /* Styling Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1F2937;
    }
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: #E2E8F0 !important;
        font-weight: 500;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-weight: 600;
        color: #00F2FE !important;
    }

    /* Elemen Pembatas / Divider */
    hr {
        margin: 2rem 0;
        border-color: #1E293B;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header Tampilan Web
st.markdown(
    """
    <div class="main-header">
        <h1>⚡ MB-VANGUARD</h1>
        <p>Manufacture Basic - Intelligent Data Validation & Unified Audit System</p>
    </div>
""",
    unsafe_allow_html=True,
)

# --- SIDEBAR NAVIGASI ---
st.sidebar.markdown("### 🧭 Menu Navigasi")
menu_pilihan = st.sidebar.radio(
    "Pilih Modul Sistem:", ["📂 Master Data (Upload)", "🚀 Proses & Analisis Data"]
)

# Inisialisasi Session State
if "processed_df" not in st.session_state:
  st.session_state.processed_df = None
if "raw_master" not in st.session_state:
  st.session_state.raw_master = None
if "raw_dyelot" not in st.session_state:
  st.session_state.raw_dyelot = None
if "benang_incorrect_kodes" not in st.session_state:
  st.session_state.benang_incorrect_kodes = set()

# --- MENU 1: MASTER DATA (UPLOAD) ---
if menu_pilihan == "📂 Master Data (Upload)":
  st.markdown("### 📂 Unggah Berkas Master Ekspor ERP & Master Resep Dyelot")
  st.write(
      "Silakan unggah berkas master ekspor gudang serta berkas Master Resep"
      " Dyelot pada panel di bawah ini."
  )

  st.markdown("#### 1. Berkas Master Ekspor Gudang (Manufacture Basic)")
  uploaded_files = st.file_uploader(
      "Pilih berkas Excel master gudang (.xlsx)",
      type=["xlsx"],
      accept_multiple_files=True,
      key="upload_mb",
  )

  st.markdown("#### 2. Berkas Master Resep / Dyelot Obat")
  uploaded_dyelot_files = st.file_uploader(
      "Pilih berkas Excel Master Dyelot / Resep (.xlsx)",
      type=["xlsx"],
      accept_multiple_files=True,
      key="upload_dyelot",
  )

  if uploaded_files:
    all_dataframes = []
    for file in uploaded_files:
      try:
        df_raw = pd.read_excel(file, header=None)
        if len(df_raw) > 8:
          df_trimmed = df_raw.iloc[4:-4].copy()
        else:
          df_trimmed = df_raw.copy()

        header_row_idx = None
        for idx, row in df_trimmed.iterrows():
          row_str = str(row.values)
          if (
              "Tanggal" in row_str
              and "Gudang" in row_str
              and "Kode" in row_str
          ):
            header_row_idx = idx
            break

        if header_row_idx is not None:
          df_trimmed.columns = df_trimmed.loc[header_row_idx]
          df_clean = df_trimmed.loc[header_row_idx + 1 :].copy()
        else:
          df_clean = df_trimmed.iloc[1:].copy()
          df_clean.columns = df_trimmed.iloc[0].values

        df_clean = df_clean.dropna(how="all")
        all_dataframes.append(df_clean)
      except Exception as e:
        st.error(f"Gagal memproses berkas MB {file.name}: {e}")

    if all_dataframes:
      master_raw_combined = pd.concat(all_dataframes, ignore_index=True)
      st.session_state.raw_master = master_raw_combined
      st.success(
          "✅ Berkas Master Gudang (MB) berhasil diunggah dan dibersihkan."
      )

  if uploaded_dyelot_files:
    all_dyelot_dfs = []
    for file in uploaded_dyelot_files:
      try:
        df_dyelot_raw = pd.read_excel(file)
        all_dyelot_dfs.append(df_dyelot_raw)
      except Exception as e:
        st.error(f"Gagal memproses berkas Dyelot {file.name}: {e}")

    if all_dyelot_dfs:
      dyelot_combined = pd.concat(all_dyelot_dfs, ignore_index=True)
      st.session_state.raw_dyelot = dyelot_combined
      st.success("✅ Berkas Master Resep Dyelot berhasil diunggah.")

  if (
      st.session_state.raw_master is not None
      or st.session_state.raw_dyelot is not None
  ):
    st.markdown("---")
    st.markdown("#### Pratinjau Data Master Gudang (MB):")
    if st.session_state.raw_master is not None:
      st.dataframe(st.session_state.raw_master.head(10), use_container_width=True)
    else:
      st.info("Belum terdapat berkas Master Gudang yang diunggah.")

    if st.session_state.raw_dyelot is not None:
      st.markdown("#### Pratinjau Data Master Resep Dyelot:")
      st.dataframe(
          st.session_state.raw_dyelot.head(10), use_container_width=True
      )

# --- MENU 2: PROSES & ANALISIS DATA ---
elif menu_pilihan == "🚀 Proses & Analisis Data":
  st.markdown("### 🚀 Eksekusi Sistem Validasi & Audit MB + Resep Dyelot")

  if st.session_state.raw_master is None:
    st.warning(
        "⚠️ Peringatan: Belum terdapat data Master Gudang yang diunggah. Silakan"
        " melakukan unggah berkas terlebih dahulu pada menu **Master Data"
        " (Upload)**."
    )
  else:
    if st.session_state.raw_dyelot is None:
      st.info(
          "ℹ️ Informasi: Berkas Master Dyelot belum diunggah. Audit resep obat"
          " khusus TBB dengan PIBC tidak akan dijalankan, namun proses"
          " validasi kuantitas standar tetap dilanjutkan."
      )

    if st.button("🚀 Jalankan Proses & Validasi Data Lengkap"):
      with st.spinner(
          "Sedang mengeksekusi validasi ganda (validasi benang & validasi obat"
          " ke Crosscheck Qty)..."
      ):
        master_df = st.session_state.raw_master.copy()

        # Bersihkan nama kolom dari spasi ekstra
        master_df.columns = [
            str(c).strip() if pd.notna(c) else f"Unnamed_{i}"
            for i, c in enumerate(master_df.columns)
        ]

        # Pemetaan Kolom Fleksibel (Keyword Matching) Master MB
        col_mapping_std = {}
        for c in master_df.columns:
          col_mapping_std[str(c).strip().upper()] = c

        col_kode_item = None
        col_nama_item = None
        col_target_qty = None
        col_target_unit = None
        col_qty = None
        col_unit = None

        for k, v in col_mapping_std.items():
          if "KODE" in k and ("ITEM" in k or "BARANG" in k):
            col_kode_item = v
          elif ("NAMA" in k or "DESKRIPSI" in k or "URAIAN" in k) and (
              "ITEM" in k or "BARANG" in k
          ):
            col_nama_item = v
          elif "TARGET" in k and "QTY" in k:
            col_target_qty = v
          elif "TARGET" in k and "UNIT" in k:
            col_target_unit = v
          elif k in ["QTY", "JUMLAH", "QUANTITY"]:
            col_qty = v
          elif k in ["UNIT", "SATUAN"]:
            col_unit = v

        if not col_kode_item:
          for k, v in col_mapping_std.items():
            if "KODE" in k:
              col_kode_item = v
              break
        if not col_nama_item:
          for k, v in col_mapping_std.items():
            if "NAMA" in k or "BARANG" in k:
              if v != col_kode_item:
                col_nama_item = v
                break
        if not col_target_qty:
          for k, v in col_mapping_std.items():
            if "TARGET" in k:
              col_target_qty = v
              break
        if not col_target_unit:
          for k, v in col_mapping_std.items():
            if "UNIT" in k and v != col_unit:
              col_target_unit = v
              break
        if not col_qty:
          for k, v in col_mapping_std.items():
            if "QTY" in k:
              col_qty = v
              break
        if not col_unit:
          for k, v in col_mapping_std.items():
            if "UNIT" in k and v != col_target_unit:
              col_unit = v
              break

        # Pastikan kolom Keterangan dan Keterangan Lain ada di dataframe
        for c_name in ["Keterangan", "Keterangan Lain"]:
          if c_name not in master_df.columns:
            master_df[c_name] = ""

        # 1. Forward Fill untuk kolom utama per Kode Transaksi
        target_ffill_cols = [
            "Gudang",
            "Kode",
            "Kode Barang Jadi",
            "Nama Barang Jadi",
            "Keterangan",
            "Keterangan Lain",
        ]
        for col in target_ffill_cols:
          if col in master_df.columns:
            if "Kode" in master_df.columns and col != "Kode":
              master_df[col] = master_df.groupby("Kode")[col].ffill()
            master_df[col] = master_df[col].ffill()

        # Fungsi konversi angka aman
        def parse_numeric(val):
          if pd.isna(val) or str(val).strip() == "":
            return None
          if isinstance(val, (int, float)):
            return float(val)
          try:
            s = str(val).strip()
            if "," in s and "." in s:
              if s.find(",") > s.find("."):
                s = s.replace(".", "").replace(",", ".")
              else:
                s = s.replace(",", "")
            elif "," in s and "." not in s:
              s = s.replace(",", ".")
            return float(s)
          except:
            return pd.to_numeric(str(val), errors="coerce")

        # 2. QTY Target Standar (GR)
        if col_target_qty and col_target_unit:
          master_df["QTY Target Standar (GR)"] = master_df.apply(
              lambda row: (
                  parse_numeric(row[col_target_qty]) * 1000
                  if str(row.get(col_target_unit, ""))
                  .strip()
                  .upper()
                  in ["KG", "KGS"]
                  else parse_numeric(row[col_target_qty])
              )
              if parse_numeric(row.get(col_target_qty)) is not None
              else "",
              axis=1,
          )
          cols = list(master_df.columns)
          if (
              "QTY Target Standar (GR)" in cols
              and col_target_unit in cols
          ):
            cols.remove("QTY Target Standar (GR)")
            tu_idx = cols.index(col_target_unit)
            cols.insert(tu_idx + 1, "QTY Target Standar (GR)")
            master_df = master_df[cols]
        else:
