# -*- coding: utf-8 -*-
"""KODE PROGRAM PROJECT CEK MB DYELOT.ipynb"""

import io
import re
import pandas as pd
import streamlit as st

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="DATA CONTROL DYEING",
    page_icon="⚡",
    layout="wide",
)

# Custom Styling CSS - Tema Modern Dark Slate & Custom Sidebar Navigation
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

    /* Styling Sidebar Elegan & Modern */
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
        padding-top: 1rem;
    }
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: #E2E8F0 !important;
    }
    
    /* Sembunyikan radio button bawaan Streamlit agar bersih */
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 10px;
    }
    section[data-testid="stSidebar"] .stRadio label {
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 12px 16px;
        border-radius: 12px;
        width: 100%;
        cursor: pointer;
        transition: all 0.25s ease;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: #334155;
        border-color: #00F2FE;
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
        <h1>⚡ DATA CONTROL DYEING</h1>
        <p>Manufacture Basic - Intelligent Data Validation & Unified Audit System</p>
    </div>
""",
    unsafe_allow_html=True,
)

# --- SIDEBAR NAVIGASI (Logo DCD) ---
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 10px 0 20px 0; border-bottom: 1px solid #1E293B; margin-bottom: 25px;">
        <h1 style="margin: 0; color: #00F2FE; font-size: 2rem; font-weight: 900; letter-spacing: 0.1em;">DCD</h1>
    </div>
""",
    unsafe_allow_html=True,
)

menu_pilihan = st.sidebar.radio(
    "Pilih Modul Sistem:",
    ["📂 Master Data (Upload)", "🚀 Proses & Analisis Data"],
    label_visibility="collapsed",
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
          master_df["QTY Target Standar (GR)"] = ""

        # 3. Qty BB Standar (GR)
        if col_qty and col_unit:
          master_df["Qty BB Standar (GR)"] = master_df.apply(
              lambda row: (
                  parse_numeric(row[col_qty]) * 1000
                  if str(row.get(col_unit, "")).strip().upper() in ["KG", "KGS"]
                  else parse_numeric(row[col_qty])
              )
              if pd.notna(row.get(col_kode_item))
              and str(row.get(col_kode_item)).strip() != ""
              and "TOTAL" not in str(row.get(col_kode_item)).upper()
              and str(row.get(col_kode_item)).strip() != "Overhead Cost"
              and parse_numeric(row.get(col_qty)) is not None
              else "",
              axis=1,
          )
          cols = list(master_df.columns)
          if "Qty BB Standar (GR)" in cols and col_qty in cols:
            cols.remove("Qty BB Standar (GR)")
            q_idx = cols.index(col_qty)
            cols.insert(q_idx + 1, "Qty BB Standar (GR)")
            master_df = master_df[cols]
        else:
          master_df["Qty BB Standar (GR)"] = ""

        # 4. Pemetaan Cek Benang (Text) per Kelompok Transaksi
        cek_jumlah_benang_list = []
        unique_kodes = master_df["Kode"].dropna().unique()

        kode_benang_mapping = {}
        for kode_trans in unique_kodes:
          sub_df = master_df[master_df["Kode"] == kode_trans]
          if sub_df.empty:
            continue
          gudang_raw = str(sub_df.iloc[0].get("Gudang", "")).strip().lower()

          if "mesin dyeing" in gudang_raw or "lab & rnd" in gudang_raw:
            if col_kode_item:
              benang_sub = sub_df[
                  sub_df[col_kode_item]
                  .astype(str)
                  .str.startswith(("TWP", "MWP", "TBM"), na=False)
              ]
              if not benang_sub.empty:
                unique_b = ", ".join(
                    benang_sub[col_kode_item].astype(str).unique()
                )
                kode_benang_mapping[kode_trans] = unique_b
              else:
                kode_benang_mapping[kode_trans] = "Tidak Ada TWP/MWP/TBM"
            else:
              kode_benang_mapping[kode_trans] = ""
          elif "softcone" in gudang_raw:
            if col_kode_item:
              benang_sub = sub_df[
                  sub_df[col_kode_item]
                  .astype(str)
                  .str.startswith(("TBB", "MBB", "MWP", "TWP", "TBM"), na=False)
              ]
              if not benang_sub.empty:
                unique_b = ", ".join(
                    benang_sub[col_kode_item].astype(str).unique()
                )
                kode_benang_mapping[kode_trans] = unique_b
              else:
                kode_benang_mapping[kode_trans] = "Tidak Ada TWP/MWP/TBM"
            else:
              kode_benang_mapping[kode_trans] = ""
          else:
            kode_benang_mapping[kode_trans] = ""

        # Pre-compute hasil crosscheck standar qty (benang) per group
        crosscheck_qty_results = {}
        benang_incorrect_kodes = set()
        keywords = [
            "AVALAN",
            "CROCHET",
            "KOR",
            "KOR ROMBE",
            "KOLONG",
            "REEBOK",
            "ROLL",
            "TALI",
            "KUR",
            "AVL",
            "CONS",
            "HTC",
        ]
        for kode_trans in unique_kodes:
          sub_df = master_df[master_df["Kode"] == kode_trans]
          if sub_df.empty:
            continue
          gudang = str(sub_df.iloc[0].get("Gudang", "")).strip().lower()
          first_row = sub_df.iloc[0]

          if "softcone" in gudang:
            valid_prefixes = ("TBB", "MBB", "TWP", "MWP", "TBM")
          elif "mesin dyeing" in gudang or "lab & rnd" in gudang:
            valid_prefixes = ("TWP", "MWP", "TBM")
          else:
            valid_prefixes = ()

          first_yarn_idx = None
          if col_kode_item:
            for idx_sub, row_sub in sub_df.iterrows():
              item_val = str(row_sub.get(col_kode_item, "")).strip().upper()
              if item_val.startswith(valid_prefixes):
                first_yarn_idx = idx_sub
                break

          if first_yarn_idx is None:
            continue

          target_val = first_row.get("QTY Target Standar (GR)", "")
          if (
              target_val == ""
              or pd.isna(target_val)
              or not isinstance(target_val, (int, float))
          ):
            continue

          target_qty = round(float(target_val), 0)

          if valid_prefixes and col_kode_item:
            benang_sub = sub_df[
                sub_df[col_kode_item]
                .astype(str)
                .str.startswith(valid_prefixes, na=False)
            ]
            if (
                not benang_sub.empty
                and "Qty BB Standar (GR)" in benang_sub.columns
            ):
              valid_qtys = pd.to_numeric(
                  benang_sub["Qty BB Standar (GR)"], errors="coerce"
              ).dropna()
            else:
              valid_qtys = pd.Series(dtype=float)
          else:
            valid_qtys = pd.Series(dtype=float)

          total_bb = round(valid_qtys.sum(), 0)
          selisih_val = target_qty - total_bb

          cols_to_check = [
              str(first_row.get("Nama Barang Jadi", "")),
              str(first_row.get("Keterangan", "")),
              str(first_row.get("Keterangan Lain", "")),
          ]
          has_keyword = False
          for col_val in cols_to_check:
            cleaned_val = re.sub(r"\s+", " ", col_val).strip().upper()
            if any(kw in cleaned_val for kw in keywords):
              has_keyword = True
              break

          if target_qty == total_bb:
            status_cc = "CORRECT"
          else:
            if has_keyword:
              status_cc = "INCORRECT (Memang Benar Selisih)"
            else:
              status_cc = "INCORRECT"
              benang_incorrect_kodes.add(kode_trans)

          crosscheck_qty_results[first_yarn_idx] = {
              "crosscheck": status_cc,
              "selisih": selisih_val,
              "satuan": "GR",
          }

        # --- Pre-compute Ringkasan Obat untuk Kolom 'List Item Kurang/Lebih' ---
        dyelot_df = st.session_state.raw_dyelot
        has_dyelot_data = dyelot_df is not None and not dyelot_df.empty

        dyelot_cols_map = {}
        d_col_dyelot1 = None
        if has_dyelot_data:
          dyelot_df.columns = [
              str(c).strip() if pd.notna(c) else f"U_{i}"
              for i, c in enumerate(dyelot_df.columns)
          ]
          for c in dyelot_df.columns:
            dyelot_cols_map[c.upper()] = c

          for c_d in dyelot_df.columns:
            c_up = str(c_d).strip().upper()
            if (
                c_up in ["DYELOT 1", "DYELOT1", "DYELOT-1"]
                or "DYELOT 1" in c_up
            ):
              d_col_dyelot1 = c_d
              break
          if not d_col_dyelot1:
            for c_d in dyelot_df.columns:
              if "DYELOT" in str(c_d).upper():
                d_col_dyelot1 = c_d
                break

        def find_dyelot_col(keywords_list):
          for kw in keywords_list:
            for k, v in dyelot_cols_map.items():
              if kw in k:
                return v
          return None

        d_col_kode = find_dyelot_col(
            ["KODE OBAT", "KODE ITEM", "KODE", "ITEM CODE"]
        )
        d_col_nama = find_dyelot_col(["OBAT", "NAMA OBAT", "NAMA", "ITEM"])
        d_col_actual = find_dyelot_col(
            ["ACTUAL", "AKTUAL", "QTY ACTUAL", "QTY"]
        )

        group_summary_dict = {}
        unique_kodes_audit = master_df["Kode"].dropna().unique()

        for kode_trans in unique_kodes_audit:
          sub_df = master_df[master_df["Kode"] == kode_trans]
          if sub_df.empty:
            continue

          first_row_sub = sub_df.iloc[0]
          gudang_raw = str(first_row_sub.get("Gudang", "")).strip().lower()
          is_valid_warehouse_for_dyelot = (
              "mesin dyeing" in gudang_raw or "lab & rnd" in gudang_raw
          )

          ket_text_combined = ""
          for col_c in master_df.columns:
            col_c_up = str(col_c).strip().upper()
            if "KETERANGAN" in col_c_up or col_c_up == "KET":
              val_c = first_row_sub.get(col_c)
              if pd.notna(val_c):
                ket_text_combined += " " + str(val_c)

          pibc_matches = re.findall(
              r"PIBC[\s\-\/]?[0-9A-Za-z\/\-_]+",
              ket_text_combined,
              re.IGNORECASE,
          )
          pibc_list = [m.upper().strip() for m in pibc_matches]

          if (
              not has_dyelot_data
              or not pibc_list
              or not is_valid_warehouse_for_dyelot
          ):
            group_summary_dict[kode_trans] = ""
            continue

          matched_dyelot_rows = pd.DataFrame()
          if not dyelot_df.empty and d_col_dyelot1:
            mask = False
            for pibc_code in pibc_list:
              mask = mask | (
                  dyelot_df[d_col_dyelot1]
                  .astype(str)
                  .str.upper()
                  .str.contains(re.escape(pibc_code), na=False)
              )
            matched_dyelot_rows = dyelot_df[mask]

          if matched_dyelot_rows.empty:
            group_summary_dict[kode_trans] = (
                "INCORRECT (PIBC tidak ditemukan pada Master Dyelot)"
            )
            continue

          issues = []
          has_any_tbb = False

          mb_tbb_dict = {}
          for _, row_item in sub_df.iterrows():
            item_code = (
                str(row_item.get(col_kode_item, "")).strip()
                if col_kode_item
                else ""
            )
            if item_code.upper().startswith("TBB"):
              has_any_tbb = True
              item_name = (
                  str(row_item.get(col_nama_item, "")).strip()
                  if col_nama_item
                  else ""
              )
              qty_mb_std = parse_numeric(
                  row_item.get("Qty BB Standar (GR)", 0)
              )
              if qty_mb_std is None:
                qty_mb_std = 0.0
              mb_tbb_dict[item_code.upper()] = {
                  "code": item_code,
                  "name": item_name,
                  "qty": qty_mb_std,
              }

          dyelot_tbb_dict = {}
          for _, d_row in matched_dyelot_rows.iterrows():
            d_k_obat = (
                str(d_row.get(d_col_kode, "")).strip() if d_col_kode else ""
            )
            if not d_k_obat and d_col_kode is None:
              for val_d in d_row.values:
                if pd.notna(val_d) and str(val_d).strip().upper().startswith(
                    "TBB"
                ):
                  d_k_obat = str(val_d).strip()
                  break

            if d_k_obat.upper().startswith("TBB"):
              d_name = (
                  str(d_row.get(d_col_nama, "")).strip()
                  if d_col_nama
                  else "OBAT"
              )
              actual_val = 0.0
              if d_col_actual:
                actual_val = (
                    parse_numeric(d_row.get(d_col_actual, 0)) or 0.0
                )
              else:
                for val_d in d_row.values:
                  parsed_val = parse_numeric(val_d)
                  if parsed_val is not None and parsed_val > 0:
                    actual_val = parsed_val
                    break
              dyelot_tbb_dict[d_k_obat.upper()] = {
                  "code": d_k_obat,
                  "name": d_name,
                  "qty": actual_val,
              }

          for code_up, data_mb in mb_tbb_dict.items():
            if code_up not in dyelot_tbb_dict:
              item_full_label = (
                  f"{data_mb['code']} {data_mb['name']}".strip()
              )
              issues.append(
                  f"Item Berlebih [{item_full_label}] {data_mb['qty']} GR"
              )

          for code_up, data_dyelot in dyelot_tbb_dict.items():
            if code_up not in mb_tbb_dict:
              item_full_label = (
                  f"{data_dyelot['code']} {data_dyelot['name']}".strip()
              )
              issues.append(
                  f"Item Kurang [{item_full_label}] {data_dyelot['qty']} GR"
              )

          if not has_any_tbb:
            group_summary_dict[kode_trans] = ""
          elif not issues:
            group_summary_dict[kode_trans] = "COMPLETE"
          else:
            group_summary_dict[kode_trans] = " | ".join(issues)

        # --- EKSEKUSI UTAMA ROW BY ROW KE DALAM KOLOM CROSSCHECK QTY ---
        crosscheck_qty_list = []
        selisih_list = []
        satuan_selisih_list = []
        list_item_kurang_lebih_list = []

        for idx, row in master_df.iterrows():
          item_code = (
              str(row.get(col_kode_item, "")).strip() if col_kode_item else ""
          )
          kode_trans = str(row.get("Kode", ""))
          gudang = str(row.get("Gudang", "")).strip().lower()
          is_valid_warehouse_for_dyelot = (
              "mesin dyeing" in gudang or "lab & rnd" in gudang
          )

          if not kode_trans or kode_trans == "nan":
            cek_jumlah_benang_list.append("")
            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            list_item_kurang_lebih_list.append("")
            continue

          # Handle khusus Gudang Dyeing STI
          if "dyeing sti" in gudang:
            item_val_upper = item_code.upper()
            valid_prefixes_sti = ("TBB", "MBB", "MWP", "TWP", "TBM")
            if item_val_upper.startswith(valid_prefixes_sti):
              if item_val_upper.startswith("TBB"):
                cek_jumlah_benang_list.append("BUKAN BENANG")
              else:
                cek_jumlah_benang_list.append("BUKAN CND")
            else:
              cek_jumlah_benang_list.append("")

            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            list_item_kurang_lebih_list.append("")
            continue

          # 1. Cek Benang Mapping (untuk baris pertama kelompok)
          first_idx = master_df[master_df["Kode"] == kode_trans].index[0]
          if idx == first_idx:
            cek_jumlah_benang_list.append(
                kode_benang_mapping.get(kode_trans, "")
            )
          else:
            cek_jumlah_benang_list.append("")

          # 2. Cek apakah baris ini adalah Item Obat (TBB) di gudang valid dengan PIBC
          ket_text_combined = ""
          for col_c in master_df.columns:
            col_c_up = str(col_c).strip().upper()
            if "KETERANGAN" in col_c_up or col_c_up == "KET":
              val_c = row.get(col_c)
              if pd.notna(val_c):
                ket_text_combined += " " + str(val_c)

          pibc_matches = re.findall(
              r"PIBC[\s\-\/]?[0-9A-Za-z\/\-_]+",
              ket_text_combined,
              re.IGNORECASE,
          )
          pibc_list = [m.upper().strip() for m in pibc_matches]

          handled_by_drug_audit = False
          if (
              item_code.upper().startswith("TBB")
              and has_dyelot_data
              and pibc_list
              and is_valid_warehouse_for_dyelot
          ):
            matched_dyelot_rows = pd.DataFrame()
            if d_col_dyelot1:
              mask = False
              for pibc_code in pibc_list:
                mask = mask | (
                    dyelot_df[d_col_dyelot1]
                    .astype(str)
                    .str.upper()
                    .str.contains(re.escape(pibc_code), na=False)
                )
              matched_dyelot_rows = dyelot_df[mask]

            qty_mb_std = (
                parse_numeric(row.get("Qty BB Standar (GR)", 0)) or 0.0
            )

            if matched_dyelot_rows.empty:
              crosscheck_qty_list.append("INCORRECT")
              selisih_list.append(qty_mb_std)
              satuan_selisih_list.append("GR")
            else:
              found_item = False
              item_matched_in_dyelot = None
              for _, d_row in matched_dyelot_rows.iterrows():
                d_k_obat = (
                    str(d_row.get(d_col_kode, "")).strip() if d_col_kode else ""
                )
                if not d_k_obat and d_col_kode is None:
                  for val_d in d_row.values:
                    if (
                        pd.notna(val_d)
                        and str(val_d).strip().upper() == item_code.upper()
                    ):
                      d_k_obat = str(val_d).strip()
                      break

                if d_k_obat.upper() == item_code.upper():
                  found_item = True
                  item_matched_in_dyelot = d_row
                  break

              if found_item and item_matched_in_dyelot is not None:
                actual_dyelot = 0.0
                if d_col_actual:
                  actual_dyelot = (
                      parse_numeric(item_matched_in_dyelot.get(d_col_actual, 0))
                      or 0.0
                  )
                else:
                  for val_d in item_matched_in_dyelot.values:
                    parsed_val = parse_numeric(val_d)
                    if parsed_val is not None and parsed_val > 0:
                      actual_dyelot = parsed_val
                      break

                diff_obat = round(qty_mb_std - actual_dyelot, 4)
                if diff_obat == 0:
                  crosscheck_qty_list.append("CORRECT")
                  selisih_list.append(0)
                  satuan_selisih_list.append("GR")
                else:
                  crosscheck_qty_list.append("INCORRECT")
                  selisih_list.append(diff_obat)
                  satuan_selisih_list.append("GR")
              else:
                crosscheck_qty_list.append("INCORRECT")
                selisih_list.append(qty_mb_std)
                satuan_selisih_list.append("GR")

            handled_by_drug_audit = True

          # 3. Jika bukan item obat dengan PIBC, jalankan Standard / Yarn Qty Check
          if not handled_by_drug_audit:
            if idx in crosscheck_qty_results:
              res = crosscheck_qty_results[idx]
              crosscheck_qty_list.append(res["crosscheck"])
              selisih_list.append(res["selisih"])
              satuan_selisih_list.append(res["satuan"])
            else:
              crosscheck_qty_list.append("")
              selisih_list.append("")
              satuan_selisih_list.append("")

          # 4. Masukkan ringkasan item kurang/lebih pada baris pertama transaksi kelompok
          if idx == first_idx:
            list_item_kurang_lebih_list.append(
                group_summary_dict.get(kode_trans, "")
            )
          else:
            list_item_kurang_lebih_list.append("")

        master_df["Cek jumlah benang"] = cek_jumlah_benang_list
        if "Kode" in master_df.columns:
          master_df["Cek jumlah benang"] = master_df["Cek jumlah benang"].replace(
              "", pd.NA
          )
          master_df["Cek jumlah benang"] = master_df.groupby("Kode")[
              "Cek jumlah benang"
          ].ffill()
          master_df["Cek jumlah benang"] = master_df[
              "Cek jumlah benang"
          ].fillna("")

        master_df["Crosscheck Qty"] = crosscheck_qty_list
        master_df["Selisih"] = selisih_list
        master_df["Satuan Selisih"] = satuan_selisih_list
        master_df["List Item Kurang/Lebih"] = list_item_kurang_lebih_list

        st.session_state.processed_df = master_df
        st.session_state.benang_incorrect_kodes = benang_incorrect_kodes
        st.success(
            "✨ Proses validasi data berhasil dieksekusi secara komprehensif."
        )

    # Tampilkan hasil & tombol download
    if st.session_state.processed_df is not None:
      processed_df = st.session_state.processed_df

      st.markdown("---")
      st.markdown("### 📊 Ringkasan Hasil Audit & Unduh Laporan")

      total_trx = len(processed_df["Kode"].dropna().unique())
      correct_count = (processed_df["Crosscheck Qty"] == "CORRECT").sum()
      incorrect_normal = (processed_df["Crosscheck Qty"] == "INCORRECT").sum()
      incorrect_wajar = (
          processed_df["Crosscheck Qty"] == "INCORRECT (Memang Benar Selisih)"
      ).sum()

      m1, m2, m3, m4 = st.columns(4)
      with m1:
        st.metric(
            label="Total Kelompok Transaksi", value=f"{total_trx:,} Transaksi"
        )
      with m2:
        st.metric(label="Status: CORRECT", value=f"{correct_count:,}")
      with m3:
        st.metric(label="Status: INCORRECT", value=f"{incorrect_normal:,}")
      with m4:
        st.metric(label="Status: Selisih Wajar", value=f"{incorrect_wajar:,}")

      st.markdown("---")

      # BAGIAN TOMBOL DOWNLOAD
      col_dl1, col_dl2 = st.columns(2)

      with col_dl1:
        output_buffer_all = io.BytesIO()
        with pd.ExcelWriter(output_buffer_all, engine="openpyxl") as writer:
          processed_df.to_excel(
              writer, index=False, sheet_name="Master_Validasi"
          )
        excel_data_all = output_buffer_all.getvalue()

        st.download_button(
            label="📥 Unduh Seluruh Berkas Laporan (Lengkap)",
            data=excel_data_all,
            file_name="Laporan_Master_Validasi_MB.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
            use_container_width=True,
        )

      with col_dl2:
        output_buffer_inc = io.BytesIO()
        with pd.ExcelWriter(output_buffer_inc, engine="openpyxl") as writer:
          kodes_incorrect = processed_df[
              (processed_df["Crosscheck Qty"] == "INCORRECT")
              & (processed_df["Kode"].notna())
              & (processed_df["Kode"] != "")
          ]["Kode"].unique()

          kodes_wajar = processed_df[
              (
                  processed_df["Crosscheck Qty"]
                  == "INCORRECT (Memang Benar Selisih)"
              )
              & (processed_df["Kode"].notna())
              & (processed_df["Kode"] != "")
          ]["Kode"].unique()

          df_inc_normal_full = processed_df[
              processed_df["Kode"].isin(kodes_incorrect)
          ]
          df_inc_wajar_full = processed_df[
              processed_df["Kode"].isin(kodes_wajar)
          ]

          benang_kodes = getattr(
              st.session_state, "benang_incorrect_kodes", set()
          )
          df_inc_benang_full = processed_df[
              processed_df["Kode"].isin(benang_kodes)
          ]

          df_inc_normal_full.to_excel(writer, index=False, sheet_name="INCORRECT")
          df_inc_wajar_full.to_excel(
              writer, index=False, sheet_name="INCORRECT (Selisih Wajar)"
          )
          df_inc_benang_full.to_excel(
              writer, index=False, sheet_name="incorrect benang"
          )
        excel_data_inc = output_buffer_inc.getvalue()

        st.download_button(
            label=(
                "📥 Unduh Rekap Kelompok INCORRECT & Benang (3 Lembar Kerja)"
            ),
            data=excel_data_inc,
            file_name="Laporan_Rekap_Incorrect_Satu_Kelompok.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
            use_container_width=True,
        )

      st.markdown("---")

      status_filter = st.selectbox(
          "🔍 Filter Tampilan Berdasarkan Status Crosscheck Qty:",
          [
              "Tampilkan Semua",
              "CORRECT",
              "INCORRECT",
              "INCORRECT (Memang Benar Selisih)",
          ],
      )

      if status_filter != "Tampilkan Semua":
        display_df = processed_df[
            processed_df["Crosscheck Qty"] == status_filter
        ]
      else:
        display_df = processed_df

      st.dataframe(display_df, use_container_width=True, height=450)
