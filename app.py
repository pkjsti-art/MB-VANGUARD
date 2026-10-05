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

# Custom Styling CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F0F8FF;
        color: #111111;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #00B4DB 0%, #0083B0 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 180, 219, 0.3);
        margin-bottom: 20px;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 5px 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 2px solid #E1E8ED;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    div[data-testid="metric-container"] label {
        color: #111111 !important;
        font-weight: 700 !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #0083B0 !important;
        font-weight: 700 !important;
    }
    div.stButton > button {
        background-color: #FFD700;
        color: #111111;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        box-shadow: 0 4px 10px rgba(255, 215, 0, 0.4);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #FFC700;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(255, 215, 0, 0.6);
    }
    section[data-testid="stSidebar"] {
        background-color: #E6F2FF;
        border-right: 1px solid #CCE4FF;
    }
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] div {
        color: #111111 !important;
        font-weight: 600;
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
st.sidebar.markdown("### 🧭 Menu Navigasi MB-VANGUARD")
menu_pilihan = st.sidebar.radio(
    "Pilih Menu:", ["📂 Master Data (Upload)", "🚀 Proses & Analisis Data"]
)

# Inisialisasi Session State
if "processed_df" not in st.session_state:
  st.session_state.processed_df = None
if "raw_master" not in st.session_state:
  st.session_state.raw_master = None
if "raw_dyelot" not in st.session_state:
  st.session_state.raw_dyelot = None


# Fungsi pembersih string kode agar kebal terhadap perbedaan titik/strip/spasi
def clean_code(val):
  if pd.isna(val):
    return ""
  return re.sub(r"[^A-Za-z0-9]", "", str(val)).upper()


# --- MENU 1: MASTER DATA (UPLOAD) ---
if menu_pilihan == "📂 Master Data (Upload)":
  st.markdown("### 📂 Unggah File Master Export ERP & Master Dyelot")
  st.write(
      "Silakan upload file master export Excel gudang serta file Master"
      " Dyelot (Resep) pada bagian di bawah ini."
  )

  st.markdown("#### 1. File Master Export Gudang (MB)")
  uploaded_files = st.file_uploader(
      "Pilih file Excel master gudang (.xlsx)",
      type=["xlsx"],
      accept_multiple_files=True,
      key="upload_mb",
  )

  st.markdown("#### 2. File Master Dyelot / Resep Obat")
  uploaded_dyelot_files = st.file_uploader(
      "Pilih file Excel Master Dyelot / Resep (.xlsx)",
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
        st.error(f"Gagal memproses file MB {file.name}: {e}")

    if all_dataframes:
      master_raw_combined = pd.concat(all_dataframes, ignore_index=True)
      st.session_state.raw_master = master_raw_combined
      st.success("✅ File Master Gudang (MB) berhasil di-upload dan dibersihkan!")

  if uploaded_dyelot_files:
    all_dyelot_dfs = []
    for file in uploaded_dyelot_files:
      try:
        df_dyelot_raw = pd.read_excel(file)
        all_dyelot_dfs.append(df_dyelot_raw)
      except Exception as e:
        st.error(f"Gagal memproses file Dyelot {file.name}: {e}")

    if all_dyelot_dfs:
      dyelot_combined = pd.concat(all_dyelot_dfs, ignore_index=True)
      st.session_state.raw_dyelot = dyelot_combined
      st.success("✅ File Master Dyelot (Resep) berhasil di-upload!")

  if (
      st.session_state.raw_master is not None
      or st.session_state.raw_dyelot is not None
  ):
    st.markdown("---")
    st.markdown("#### Preview Data Master Gudang (MB):")
    if st.session_state.raw_master is not None:
      st.dataframe(st.session_state.raw_master.head(10), use_container_width=True)
    else:
      st.info("Belum ada file Master Gudang yang di-upload.")

    if st.session_state.raw_dyelot is not None:
      st.markdown("#### Preview Data Master Dyelot (Resep):")
      st.dataframe(
          st.session_state.raw_dyelot.head(10), use_container_width=True
      )

# --- MENU 2: PROSES & ANALISIS DATA ---
elif menu_pilihan == "🚀 Proses & Analisis Data":
  st.markdown("### 🚀 Eksekusi Sistem Validasi & Audit MB + Resep Dyelot")

  if st.session_state.raw_master is None:
    st.warning(
        "⚠️ Belum ada data Master Gudang yang di-upload. Silakan lakukan upload"
        " di menu **Master Data (Upload)** terlebih dahulu!"
    )
  else:
    if st.session_state.raw_dyelot is None:
      st.warning(
          "⚠️ Perhatian: File Master Dyelot belum di-upload. Audit obat akan"
          " dilewati jika file resep belum disertakan."
      )

    if st.button("🚀 Jalankan Proses & Validasi Data Lengkap"):
      with st.spinner("Sedang mengeksekusi rumus dan audit resep/obat akurat..."):
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

        # Forward Fill untuk kolom utama per Kode Transaksi
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


        # QTY Target Standar (GR) - Tampilan Asli (Tidak di-forward fill)
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

        # KOLOM BANTU INTERNAL (Di-ffill khusus untuk backend kalkulasi tanpa merusak tampilan asli)
        if "Kode" in master_df.columns and "QTY Target Standar (GR)" in master_df.columns:
          master_df["_temp_target_gr"] = master_df["QTY Target Standar (GR)"].copy()
          master_df["_temp_target_gr"] = master_df.groupby("Kode")[
              "_temp_target_gr"
          ].ffill().bfill()
        else:
          master_df["_temp_target_gr"] = master_df["QTY Target Standar (GR)"]

        # Qty BB Standar (GR)
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

        # --- SETUP MASTER DYELOT & DICTIONARY AUDIT OBAT ---
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

        unique_kodes = master_df["Kode"].dropna().unique()
        group_summary_dict = {}

        for kode_trans in unique_kodes:
          sub_df = master_df[master_df["Kode"] == kode_trans]
          if sub_df.empty:
            continue

          first_row_sub = sub_df.iloc[0]
          gudang_row_val = str(first_row_sub.get("Gudang", "")).strip().lower()

          # Audit obat hanya dijalankan jika gudang Mesin Dyeing atau Lab & Rnd
          if not (
              "mesin dyeing" in gudang_row_val or "lab & rnd" in gudang_row_val
          ):
            group_summary_dict[kode_trans] = ""
            continue

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

          # Jika tidak ada PIBC, resep obat di-skip
          if not has_dyelot_data or not pibc_list:
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
                "INCORRECT (PIBC tidak ditemukan di Master Dyelot)"
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
              mb_tbb_dict[clean_code(item_code)] = {
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
                if pd.notna(val_d) and clean_code(val_d).startswith("TBB"):
                  d_k_obat = str(val_d).strip()
                  break

            if clean_code(d_k_obat).startswith("TBB"):
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
              dyelot_tbb_dict[clean_code(d_k_obat)] = {
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
                  f"Item Berlebihan [{item_full_label}] {data_mb['qty']} GR"
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

        # Mapping item benang & pencarian index baris benang pertama KHUSUS Mesin Dyeing & Lab & Rnd
        first_yarn_idx_dict = {}
        kode_benang_mapping = {}

        for kode_trans in unique_kodes:
          sub_df = master_df[master_df["Kode"] == kode_trans]
          if sub_df.empty:
            continue
          gudang_raw = str(sub_df.iloc[0].get("Gudang", "")).strip().lower()

          if "mesin dyeing" in gudang_raw or "lab & rnd" in gudang_raw:
            if col_kode_item:
              # Menggunakan .str.strip().str.upper() agar tahan terhadap spasi/huruf kecil di ERP
              benang_sub = sub_df[
                  sub_df[col_kode_item]
                  .astype(str)
                  .str.strip()
                  .str.upper()
                  .str.startswith(("TWP", "MWP", "TBM"), na=False)
              ]
              if not benang_sub.empty:
                unique_b = ", ".join(
                    benang_sub[col_kode_item].astype(str).str.strip().unique()
                )
                kode_benang_mapping[kode_trans] = unique_b
                # Mengambil index baris item benang PERTAMA (bisa di baris ke-2, ke-3, dst)
                first_yarn_idx_dict[kode_trans] = benang_sub.index[0]
              else:
                kode_benang_mapping[kode_trans] = "Tidak Ada TWP/MWP/TBM"
            else:
              kode_benang_mapping[kode_trans] = ""

        # --- ITERASI UTAMA PER BARIS UNTUK MENGISI KOLOM UTAMA ---
        cek_jumlah_benang_list = []
        crosscheck_qty_list = []
        selisih_list = []
        satuan_selisih_list = []
        list_item_kurang_lebih_list = []

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
        ]

        for idx, row in master_df.iterrows():
          kode_trans = str(row.get("Kode", ""))
          gudang = str(row.get("Gudang", "")).strip().lower()
          item_code = (
              str(row.get(col_kode_item, "")).strip() if col_kode_item else ""
          )

          if not kode_trans or kode_trans == "nan":
            cek_jumlah_benang_list.append("")
            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            list_item_kurang_lebih_list.append("")
            continue

          first_idx = (
              master_df[master_df["Kode"] == kode_trans].index[0]
              if kode_trans in master_df["Kode"].values
              else -1
          )
          is_first_yarn_row = idx == first_yarn_idx_dict.get(kode_trans)

          # PENEMPATAN TEKS KODE BENANG & SUMMARY DI BARIS BENANG PERTAMA ATAU BARIS PERTAMA
          if is_first_yarn_row:
            cek_jumlah_benang_list.append(
                kode_benang_mapping.get(kode_trans, "")
            )
            list_item_kurang_lebih_list.append(
                group_summary_dict.get(kode_trans, "")
            )
          elif idx == first_idx and kode_trans not in first_yarn_idx_dict:
            cek_jumlah_benang_list.append(
                kode_benang_mapping.get(kode_trans, "")
            )
            list_item_kurang_lebih_list.append(
                group_summary_dict.get(kode_trans, "")
            )
          else:
            cek_jumlah_benang_list.append("")
            list_item_kurang_lebih_list.append("")

          # Hanya proses gudang Mesin Dyeing & Lab & Rnd
          if not ("mesin dyeing" in gudang or "lab & rnd" in gudang):
            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            continue

          is_tbb_item = item_code.upper().startswith("TBB")

          cc_val = ""
          sel_val = ""
          sat_val = ""

          # A. Cek Benang (Group-Level Qty Check) - BERJALAN DI BARIS BENANG PERTAMA (BAIK DI ATAS MAUPUN DI BAWAH)
          if is_first_yarn_row:
            target_val = row.get("_temp_target_gr", "")
            if (
                target_val != ""
                and pd.notna(target_val)
                and isinstance(target_val, (int, float))
            ):
              target_qty = round(float(target_val), 0)
              sub_df = master_df[master_df["Kode"] == kode_trans]
              benang_sub = (
                  sub_df[
                      sub_df[col_kode_item]
                      .astype(str)
                      .str.strip()
                      .str.upper()
                      .str.startswith(("TWP", "MWP", "TBM"), na=False)
                  ]
                  if col_kode_item
                  else pd.DataFrame()
              )

              if (
                  not benang_sub.empty
                  and "Qty BB Standar (GR)" in benang_sub.columns
              ):
                valid_qtys = pd.to_numeric(
                    benang_sub["Qty BB Standar (GR)"], errors="coerce"
                ).dropna()
              else:
                valid_qtys = pd.Series(dtype=float)

              total_bb = round(valid_qtys.sum(), 0)
              diff_group = target_qty - total_bb

              cols_to_check = [
                  str(row.get("Nama Barang Jadi", "")),
                  str(row.get("Keterangan", "")),
                  str(row.get("Keterangan Lain", "")),
              ]
              has_keyword = False
              for col_val in cols_to_check:
                cleaned_val = re.sub(r"\s+", " ", col_val).strip().upper()
                if any(kw in cleaned_val for kw in keywords):
                  has_keyword = True
                  break

              if target_qty == total_bb:
                cc_val = "CORRECT"
                sel_val = diff_group
                sat_val = "GR"
              else:
                if has_keyword:
                  cc_val = "INCORRECT (Memang Benar Selisih)"
                else:
                  cc_val = "INCORRECT"
                sel_val = diff_group
                sat_val = "GR"

          # B. Cek Obat TBB (Item-Level Medicine Audit) - HANYA JIKA ADA PIBC DAN DYELOT
          elif is_tbb_item and has_dyelot_data:
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

            if pibc_list:
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
                cc_val = "INCORRECT"
                qty_mb_std = (
                    parse_numeric(row.get("Qty BB Standar (GR)", 0)) or 0.0
                )
                sel_val = qty_mb_std
                sat_val = "GR"
              else:
                found_item = False
                item_matched_in_dyelot = None
                clean_item_code = clean_code(item_code)

                for _, d_row in matched_dyelot_rows.iterrows():
                  d_k_obat = (
                      str(d_row.get(d_col_kode, "")).strip()
                      if d_col_kode
                      else ""
                  )
                  if not d_k_obat and d_col_kode is None:
                    for val_d in d_row.values:
                      if (
                          pd.notna(val_d)
                          and clean_code(val_d) == clean_item_code
                      ):
                        d_k_obat = str(val_d).strip()
                        break

                  if clean_code(d_k_obat) == clean_item_code:
                    found_item = True
                    item_matched_in_dyelot = d_row
                    break

                qty_mb_std = (
                    parse_numeric(row.get("Qty BB Standar (GR)", 0)) or 0.0
                )

                if found_item and item_matched_in_dyelot is not None:
                  actual_dyelot = 0.0
                  if d_col_actual:
                    actual_dyelot = (
                        parse_numeric(
                            item_matched_in_dyelot.get(d_col_actual, 0)
                        )
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
                    cc_val = "CORRECT"
                    sel_val = 0
                    sat_val = "GR"
                  else:
                    cc_val = "INCORRECT"
                    sel_val = diff_obat
                    sat_val = "GR"
                else:
                  cc_val = "INCORRECT"
                  sel_val = qty_mb_std
                  sat_val = "GR"

          crosscheck_qty_list.append(cc_val)
          selisih_list.append(sel_val)
          satuan_selisih_list.append(sat_val)

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

        # Hapus kolom sementara _temp_target_gr agar tidak ikut tampil di layar / export Excel
        if "_temp_target_gr" in master_df.columns:
          master_df = master_df.drop(columns=["_temp_target_gr"])

        st.session_state.processed_df = master_df
        st.success("✨ Proses validasi dan audit resep obat berhasil dijalankan!")

    # Tampilkan hasil & tombol download
    if st.session_state.processed_df is not None:
      processed_df = st.session_state.processed_df

      st.markdown("---")
      st.markdown("### 📊 Ringkasan Hasil Audit & Download Laporan")

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
            label="📥 Download Semua Data (Lengkap)",
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

          df_inc_normal_full.to_excel(writer, index=False, sheet_name="INCORRECT")
          df_inc_wajar_full.to_excel(
              writer, index=False, sheet_name="INCORRECT (Selisih Wajar)"
          )
        excel_data_inc = output_buffer_inc.getvalue()

        st.download_button(
            label="📥 Download Rekap 1 Kelompok INCORRECT (2 Sheet)",
            data=excel_data_inc,
            file_name="Laporan_Rekap_Incorrect_Satu_Kelompok.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
            use_container_width=True,
        )

      st.markdown("---")

      status_filter = filter_val = st.selectbox(
          "🔍 Filter Tampilan Berdasarkan Status:",
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
