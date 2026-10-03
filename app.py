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

# --- MENU 1: MASTER DATA (UPLOAD) ---
if menu_pilihan == "📂 Master Data (Upload)":
  st.markdown("### 📂 Unggah File Master Export ERP Gudang")
  st.write(
      "Silakan upload semua file master export Excel dari berbagai gudang"
      " secara bersamaan."
  )

  uploaded_files = st.file_uploader(
      "Pilih file Excel master gudang (.xlsx)",
      type=["xlsx"],
      accept_multiple_files=True,
  )

  if uploaded_files:
    all_dataframes = []

    for file in uploaded_files:
      try:
        df_raw = pd.read_excel(file, header=None)

        # Hapus 4 baris paling atas dan 4 baris paling bawah
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
        st.error(f"Gagal memproses file {file.name}: {e}")

    if all_dataframes:
      master_raw_combined = pd.concat(all_dataframes, ignore_index=True)
      st.session_state.raw_master = master_raw_combined
      st.success(
          "✅ File berhasil di-upload dan dibersihkan! Silakan pindah ke menu"
          " **Proses & Analisis Data** di sidebar."
      )

      st.markdown("#### Preview Data Mentah:")
      st.dataframe(master_raw_combined.head(15), use_container_width=True)

# --- MENU 2: PROSES & ANALISIS DATA ---
elif menu_pilihan == "🚀 Proses & Analisis Data":
  st.markdown("### 🚀 Eksekusi Sistem Validasi & Audit MB")

  if st.session_state.raw_master is None:
    st.warning(
        "⚠️ Belum ada data yang di-upload. Silakan lakukan upload file di menu"
        " **Master Data (Upload)** terlebih dahulu!"
    )
  else:
    if st.button("🚀 Jalankan Proses & Validasi Data"):
      with st.spinner("Sedang mengeksekusi rumus dan logika audit akurat..."):
        master_df = st.session_state.raw_master.copy()

        # Bersihkan nama kolom dari spasi ekstra
        master_df.columns = [
            str(c).strip() if pd.notna(c) else f"Unnamed_{i}"
            for i, c in enumerate(master_df.columns)
        ]

        # Pemetaan Kolom Fleksibel (Keyword Matching)
        col_mapping_std = {}
        for c in master_df.columns:
          col_mapping_std[str(c).strip().upper()] = c

        col_kode_item = None
        col_target_qty = None
        col_target_unit = None
        col_qty = None
        col_unit = None

        for k, v in col_mapping_std.items():
          if "KODE" in k and ("ITEM" in k or "BARANG" in k):
            col_kode_item = v
          elif "TARGET" in k and "QTY" in k:
            col_target_qty = v
          elif "TARGET" in k and "UNIT" in k:
            col_target_unit = v
          elif k in ["QTY", "JUMLAH", "QUANTITY"]:
            col_qty = v
          elif k in ["UNIT", "SATUAN"]:
            col_unit = v

        # Fallback pencarian fleksibel
        if not col_kode_item:
          for k, v in col_mapping_std.items():
            if "KODE" in k:
              col_kode_item = v
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

        st.info(
            f"ℹ️ **Deteksi Kolom Otomatis:** Kode Item=`{col_kode_item}` | Target"
            f" Qty=`{col_target_qty}` | Target Unit=`{col_target_unit}` |"
            f" Qty=`{col_qty}` | Unit=`{col_unit}`"
        )

        # 1. Forward Fill untuk kolom: Gudang, Kode, Kode Barang Jadi, Nama Barang Jadi
        target_ffill_cols = [
            "Gudang",
            "Kode",
            "Kode Barang Jadi",
            "Nama Barang Jadi",
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

        # Pastikan kolom teks pendukung aman
        for c_name in [
            "Keterangan",
            "Keterangan Lain",
            "Nama Barang Jadi",
            col_kode_item,
        ]:
          if c_name and c_name not in master_df.columns:
            master_df[c_name] = ""

        # 4. Pemetaan Cek Benang, Crosscheck Qty, dan Selisih per Kelompok Transaksi
        cek_jumlah_benang_list = []
        crosscheck_qty_list = []
        selisih_list = []
        satuan_selisih_list = []

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

        for idx, row in master_df.iterrows():
          kode_trans = str(row.get("Kode", ""))
          gudang = str(row.get("Gudang", "")).strip().lower()

          if not kode_trans or kode_trans == "nan":
            cek_jumlah_benang_list.append("")
            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            continue

          # ATURAN GUDANG DYEING STI
          if "dyeing sti" in gudang:
            item_val = (
                str(row.get(col_kode_item, "")).strip() if col_kode_item else ""
            )
            item_val_upper = item_val.upper()

            valid_prefixes = ("TBB", "MBB", "MWP", "TWP", "TBM")
            if item_val_upper.startswith(valid_prefixes):
              if item_val_upper.startswith("TBB"):
                cek_jumlah_benang_list.append("BUKAN BENANG")
              else:
                cek_jumlah_benang_list.append("BUKAN CND")
            else:
              cek_jumlah_benang_list.append("")

            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            continue

          # Untuk gudang selain Gudang dyeing STI
          first_idx = master_df[master_df["Kode"] == kode_trans].index[0]
          if idx == first_idx:
            cek_jumlah_benang_list.append(
                kode_benang_mapping.get(kode_trans, "")
            )
          else:
            cek_jumlah_benang_list.append("")

          if idx != first_idx:
            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            continue

          target_val = row.get("QTY Target Standar (GR)", "")
          if (
              target_val == ""
              or pd.isna(target_val)
              or not isinstance(target_val, (int, float))
          ):
            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            continue

          target_qty = round(float(target_val), 0)
          sub_df = master_df[master_df["Kode"] == kode_trans]

          if "softcone" in gudang:
            benang_sub = (
                sub_df[
                    sub_df[col_kode_item]
                    .astype(str)
                    .str.startswith(
                        ("TBB", "MBB", "TWP", "MWP", "TBM"), na=False
                    )
                ]
                if col_kode_item
                else pd.DataFrame()
            )
          elif "mesin dyeing" in gudang or "lab & rnd" in gudang:
            benang_sub = (
                sub_df[
                    sub_df[col_kode_item]
                    .astype(str)
                    .str.startswith(("TWP", "MWP", "TBM"), na=False)
                ]
                if col_kode_item
                else pd.DataFrame()
            )
          else:
            benang_sub = pd.DataFrame()

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
          selisih_val = target_qty - total_bb

          # PENGECEKAN KATA KUNCI DI 3 KOLOM SECARA INDEPENDEN & FLEKSIBEL
          cols_to_check = [
              str(row.get("Nama Barang Jadi", "")),
              str(row.get("Keterangan", "")),
              str(row.get("Keterangan Lain", "")),
          ]

          has_keyword = False
          for col_val in cols_to_check:
            cleaned_val = re.sub(r'\s+', ' ', col_val).strip().upper()
            if any(kw in cleaned_val for kw in keywords):
              has_keyword = True
              break

          if target_qty == total_bb:
            crosscheck_qty_list.append("CORRECT")
            selisih_list.append(selisih_val)
            satuan_selisih_list.append("GR")
          else:
            if has_keyword:
              crosscheck_qty_list.append("INCORRECT (Memang Benar Selisih)")
            else:
              crosscheck_qty_list.append("INCORRECT")
            selisih_list.append(selisih_val)
            satuan_selisih_list.append("GR")

        master_df["Cek jumlah benang"] = cek_jumlah_benang_list
        
        # Forward fill kolom "Cek jumlah benang" per kelompok transaksi (Kode)
        if "Kode" in master_df.columns:
          master_df["Cek jumlah benang"] = master_df["Cek jumlah benang"].replace("", pd.NA)
          master_df["Cek jumlah benang"] = master_df.groupby("Kode")["Cek jumlah benang"].ffill()
          master_df["Cek jumlah benang"] = master_df["Cek jumlah benang"].fillna("")

        master_df["Crosscheck Qty"] = crosscheck_qty_list
        master_df["Selisih"] = selisih_list
        master_df["Satuan Selisih"] = satuan_selisih_list

        st.session_state.processed_df = master_df
        st.success("✨ Proses validasi berhasil dijalankan!")

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
        st.metric(
            label="Status: Selisih Wajar", value=f"{incorrect_wajar:,}"
        )

      st.markdown("---")

      # BAGIAN TOMBOL DOWNLOAD (2 OPSI DOWNLOAD)
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
          # Ambil daftar Kode yang statusnya INCORRECT (hanya dari baris pertama kelompok transaksi)
          kodes_incorrect = processed_df[
              (processed_df["Crosscheck Qty"] == "INCORRECT") & 
              (processed_df["Kode"].notna()) & 
              (processed_df["Kode"] != "")
          ]["Kode"].unique()

          # Ambil daftar Kode yang statusnya INCORRECT (Memang Benar Selisih)
          kodes_wajar = processed_df[
              (processed_df["Crosscheck Qty"] == "INCORRECT (Memang Benar Selisih)") & 
              (processed_df["Kode"].notna()) & 
              (processed_df["Kode"] != "")
          ]["Kode"].unique()

          # Filter seluruh baris yang memiliki Kode tersebut (satu kelompok data MB utuh)
          df_inc_normal_full = processed_df[processed_df["Kode"].isin(kodes_incorrect)]
          df_inc_wajar_full = processed_df[processed_df["Kode"].isin(kodes_wajar)]

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

      status_filter = st.selectbox(
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
