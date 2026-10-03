import io
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

        header_row_idx = None
        for idx, row in df_raw.iterrows():
          row_str = str(row.values)
          if (
              "Tanggal" in row_str
              and "Gudang" in row_str
              and "Kode" in row_str
          ):
            header_row_idx = idx
            break

        if header_row_idx is not None:
          df_raw.columns = df_raw.iloc[header_row_idx]
          df_clean = df_raw.iloc[header_row_idx + 1 :].copy()
        else:
          df_clean = df_raw.iloc[4:].copy()
          df_clean.columns = df_raw.iloc[3]
          df_clean = df_clean.iloc[1:].copy()

        df_clean = df_clean.dropna(how="all")
        all_dataframes.append(df_clean)
      except Exception as e:
        st.error(f"Gagal memproses file {file.name}: {e}")

    if all_dataframes:
      master_raw_combined = pd.concat(all_dataframes, ignore_index=True)
      st.session_state.raw_master = master_raw_combined
      st.success(
          "✅ File berhasil di-upload dan dibersihkan! Seluruh baris transaksi"
          " dipertahankan lengkap. Silakan pindah ke menu **Proses & Analisis"
          " Data** di sidebar."
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

        # Bersihkan spasi di nama kolom
        master_df.columns = [
            str(c).strip() if pd.notna(c) else f"Unnamed_{i}"
            for i, c in enumerate(master_df.columns)
        ]

        # Deteksi Kolom secara Fleksibel (Mencegah kolom tidak terbaca)
        col_kode_item = None
        col_nama_item = None
        col_target_qty = None
        col_target_unit = None
        col_qty = None
        col_unit = None

        for c in master_df.columns:
          c_up = c.upper()
          if "KODE" in c_up and ("ITEM" in c_up or "BAHAN" in c_up):
            col_kode_item = c
          elif "NAMA" in c_up and ("ITEM" in c_up or "BAHAN" in c_up):
            col_nama_item = c
          elif "TARGET" in c_up and "QTY" in c_up:
            col_target_qty = c
          elif "TARGET" in c_up and "UNIT" in c_up:
            col_target_unit = c
          elif c_up == "QTY" or (
              "QTY" in c_up and "TARGET" not in c_up and "BB" not in c_up
          ):
            col_qty = c
          elif c_up == "UNIT" or (
              "UNIT" in c_up and "TARGET" not in c_up and "SATUAN" in c_up
          ):
            col_unit = c

        # Fallback jika penamaan kolom sangat berbeda
        if not col_kode_item:
          master_df["Kode Item"] = ""
          col_kode_item = "Kode Item"
        if not col_nama_item:
          master_df["Nama Item"] = ""
          col_nama_item = "Nama Item"

        # 1. Forward Fill kolom identitas agar kelompok transaksi tetap terbaca utuh
        fill_cols = [
            "Gudang",
            "Kode",
            "Status",
            "Kode BOM",
            "Kode Barang Jadi",
            "Nama Barang Jadi",
        ]
        for col in fill_cols:
          if col in master_df.columns:
            master_df[col] = master_df[col].ffill()

        # 2. QTY Target Standar (GR)
        if col_target_qty and col_target_unit:
          master_df["QTY Target Standar (GR)"] = master_df.apply(
              lambda row: (
                  pd.to_numeric(row[col_target_qty], errors="coerce") * 1000
                  if str(row[col_target_unit]).strip().upper() == "KG"
                  else pd.to_numeric(row[col_target_qty], errors="coerce")
              )
              if pd.notna(row.get(col_target_qty))
              and str(row.get(col_target_qty)).strip() != ""
              else "",
              axis=1,
          )
          cols = list(master_df.columns)
          if (
              "QTY Target Standar (GR)" in cols
              and col_target_unit in cols
          ):
            cols.remove("QTY Target Standar (GR)")
            target_unit_idx = cols.index(col_target_unit)
            cols.insert(target_unit_idx + 1, "QTY Target Standar (GR)")
            master_df = master_df[cols]
        else:
          master_df["QTY Target Standar (GR)"] = ""

        # 3. Qty BB Standar (GR)
        if col_qty and col_unit:
          master_df["Qty BB Standar (GR)"] = master_df.apply(
              lambda row: (
                  pd.to_numeric(row[col_qty], errors="coerce") * 1000
                  if str(row[col_unit]).strip().upper() == "KG"
                  else pd.to_numeric(row[col_qty], errors="coerce")
              )
              if pd.notna(row.get(col_kode_item))
              and str(row.get(col_kode_item)).strip() != ""
              and "TOTAL" not in str(row.get(col_kode_item)).upper()
              and str(row.get(col_kode_item)).strip() != "Overhead Cost"
              and pd.notna(row.get(col_qty))
              and str(row.get(col_qty)).strip() != ""
              else "",
              axis=1,
          )
          cols = list(master_df.columns)
          if "Qty BB Standar (GR)" in cols and col_qty in cols:
            cols.remove("Qty BB Standar (GR)")
            qty_idx = cols.index(col_qty)
            cols.insert(qty_idx + 1, "Qty BB Standar (GR)")
            master_df = master_df[cols]
        else:
          master_df["Qty BB Standar (GR)"] = ""

        # Pastikan kolom teks aman
        for col_name in [
            "Keterangan",
            "Keterangan Lain",
            "Nama Barang Jadi",
            col_kode_item,
        ]:
          if col_name not in master_df.columns:
            master_df[col_name] = ""

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
        ]
        unique_kodes = master_df["Kode"].dropna().unique()

        kode_benang_mapping = {}
        for kode_trans in unique_kodes:
          sub_df = master_df[master_df["Kode"] == kode_trans]
          if sub_df.empty:
            continue
          gudang_val = str(sub_df.iloc[0].get("Gudang", "")).strip()

          if gudang_val == "Gudang dyeing STI":
            item_list = sub_df[col_kode_item].dropna().astype(str).tolist()
            if not item_list:
              kode_benang_mapping[kode_trans] = "BUKAN BENANG"
            else:
              all_tbb = all(item.startswith("TBB") for item in item_list)
              if all_tbb:
                kode_benang_mapping[kode_trans] = "BUKAN BENANG"
              else:
                kode_benang_mapping[kode_trans] = "BUKAN CND"
          elif gudang_val in ["Gudang mesin dyeing", "GUDANG LAB & RnD"]:
            benang_sub = sub_df[
                sub_df[col_kode_item]
                .astype(str)
                .str.startswith(("TWP", "MWP", "TBM"), na=False)
            ]
            if not benang_sub.empty:
              unique_b = ", ".join(benang_sub[col_kode_item].astype(str).unique())
              kode_benang_mapping[kode_trans] = unique_b
            else:
              kode_benang_mapping[kode_trans] = "Tidak Ada TWP/MWP/TBM"
          elif gudang_val == "PRODUKSI SOFTCONE":
            benang_sub = sub_df[
                sub_df[col_kode_item]
                .astype(str)
                .str.startswith(("TBB", "MBB", "MWP", "TWP", "TBM"), na=False)
            ]
            if not benang_sub.empty:
              unique_b = ", ".join(benang_sub[col_kode_item].astype(str).unique())
              kode_benang_mapping[kode_trans] = unique_b
            else:
              kode_benang_mapping[kode_trans] = "Tidak Ada TWP/MWP/TBM"
          else:
            kode_benang_mapping[kode_trans] = ""

        for idx, row in master_df.iterrows():
          kode_trans = str(row.get("Kode", ""))
          gudang = str(row.get("Gudang", "")).strip()

          if not kode_trans or kode_trans == "nan":
            cek_jumlah_benang_list.append("")
            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            continue

          cek_jumlah_benang_list.append(kode_benang_mapping.get(kode_trans, ""))

          if gudang == "Gudang dyeing STI":
            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            continue

          first_idx = master_df[master_df["Kode"] == kode_trans].index[0]
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

          if gudang == "PRODUKSI SOFTCONE":
            benang_sub = sub_df[
                sub_df[col_kode_item]
                .astype(str)
                .str.startswith(("TBB", "MBB", "TWP", "MWP", "TBM"), na=False)
            ]
          elif gudang in ["Gudang mesin dyeing", "GUDANG LAB & RnD"]:
            benang_sub = sub_df[
                sub_df[col_kode_item]
                .astype(str)
                .str.startswith(("TWP", "MWP", "TBM"), na=False)
            ]
          else:
            benang_sub = pd.DataFrame()

          valid_qtys = pd.to_numeric(
              benang_sub["Qty BB Standar (GR)"], errors="coerce"
          ).dropna()
          total_bb = round(valid_qtys.sum(), 0)

          selisih_val = target_qty - total_bb

          nama_brg_jdi = str(row.get("Nama Barang Jadi", ""))
          ket = str(row.get("Keterangan", ""))
          ket_lain = str(row.get("Keterangan Lain", ""))
          combined_text = f"{nama_brg_jdi} {ket} {ket_lain}".upper()
          has_keyword = any(kw in combined_text for kw in keywords)

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
        master_df["Crosscheck Qty"] = crosscheck_qty_list
        master_df["Selisih"] = selisih_list
        master_df["Satuan Selisih"] = satuan_selisih_list

        st.session_state.processed_df = master_df
        st.success("✨ Proses validasi berhasil dijalankan!")

    # Tampilkan hasil & tombol download
    if st.session_state.processed_df is not None:
      processed_df = st.session_state.processed_df

      st.markdown("---")
      col_dl1, col_dl2 = st.columns([2, 1])
      with col_dl1:
        st.markdown("### 📊 Ringkasan Hasil Audit")
      with col_dl2:
        output_buffer = io.BytesIO()
        with pd.ExcelWriter(output_buffer, engine="openpyxl") as writer:
          processed_df.to_excel(
              writer, index=False, sheet_name="Master_Validasi"
          )
        excel_data = output_buffer.getvalue()

        st.download_button(
            label="📥 Download Laporan Excel",
            data=excel_data,
            file_name="Laporan_Master_Validasi_MB.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        )

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
