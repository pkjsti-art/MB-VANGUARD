import io
import pandas as pd
import streamlit as st

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="MB-VANGUARD | Audit Data Manufacture Basic",
    page_icon="⚡",
    layout="wide",
)

# Custom Styling CSS (Perbaikan kontras teks sidebar & card menjadi hitam/gelap)
st.markdown(
    """
    <style>
    /* Global Styling - Blue Sky & Putih */
    .stApp {
        background-color: #F0F8FF;
        color: #111111;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header Utama */
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

    /* Memastikan Teks di dalam Card/Metric Streamlit Terlihat Jelas (Hitam di atas Putih) */
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

    /* Tombol Kustom dengan Aksen Kuning Futuristik */
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

    /* Sidebar Styling & Perbaikan Warna Teks Sidebar agar Jelas (Hitam/Gelap) */
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
        # Membaca file Excel tanpa header dulu untuk pembersihan 4 baris header ERP
        df_raw = pd.read_excel(file, header=None)

        # 1. Membersihkan baris header ERP (mencari baris yang mengandung 'Tanggal', 'Gudang', 'Kode')
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
          df_clean.iloc[1:].copy()

        # 2. Hanya membersihkan sel/baris kosong di kolom 'Kode Item' di setiap akhir kelompok data (tanpa menghapus baris transaksi penting)
        if "Kode Item" in df_clean.columns:
          # Buang baris di mana Kode Item kosong total DAN bukan bagian dari ringkasan total harga
          df_clean = df_clean[
              ~(
                  df_clean["Kode Item"].isna()
                  & df_clean["Nama Item"].isna()
                  & df_clean["Qty"].isna()
              )
          ]

        all_dataframes.append(df_clean)
      except Exception as e:
        st.error(f"Gagal memproses file {file.name}: {e}")

    if all_dataframes:
      master_raw_combined = pd.concat(all_dataframes, ignore_index=True)
      st.session_state.raw_master = master_raw_combined
      st.success(
          "✅ File berhasil di-upload dan dibersihkan dari header ERP!"
          " Silakan pindah ke menu **Proses & Analisis Data** di sidebar."
      )

      st.markdown("#### Preview Data Mentah Setelah Pembersihan Awal:")
      st.dataframe(master_raw_combined.head(10), use_container_width=True)

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
      with st.spinner(
          "Sedang memproses forward fill, penempatan kolom, dan rumus"
          " audit..."
      ):
        master_df = st.session_state.raw_master.copy()

        # 1. Forward Fill kolom identitas agar kelompok transaksi tetap utuh
        fill_cols = [
            "Gudang",
            "Kode",
            "Status",
            "Kode Barang Jadi",
            "Nama Barang Jadi",
        ]
        for col in fill_cols:
          if col in master_df.columns:
            master_df[col] = master_df[col].ffill()

        # 2. Standarisasi Qty Target Standar (GR) & posisikan di sebelah kanan kolom Target Unit
        if (
            "Target Qty" in master_df.columns
            and "Target Unit" in master_df.columns
        ):
          master_df["QTY Target Standar (GR)"] = master_df.apply(
              lambda row: (
                  pd.to_numeric(row["Target Qty"], errors="coerce") * 1000
                  if str(row["Target Unit"]).strip().upper() == "KG"
                  else pd.to_numeric(row["Target Qty"], errors="coerce")
              ),
              axis=1,
          )
          # Mengatur ulang posisi kolom agar QTY Target Standar (GR) tepat di sebelah kanan Target Unit
          cols = list(master_df.columns)
          if (
              "QTY Target Standar (GR)" in cols
              and "Target Unit" in cols
          ):
            cols.remove("QTY Target Standar (GR)")
            target_unit_idx = cols.index("Target Unit")
            cols.insert(target_unit_idx + 1, "QTY Target Standar (GR)")
            master_df = master_df[cols]
        else:
          master_df["QTY Target Standar (GR)"] = 0

        # 3. Standarisasi Qty Bahan Baku Standar (GR) & posisikan di sebelah kanan kolom Qty
        if "Qty" in master_df.columns and "Unit" in master_df.columns:
          master_df["Qty BB Standar (GR)"] = master_df.apply(
              lambda row: (
                  pd.to_numeric(row["Qty"], errors="coerce") * 1000
                  if str(row["Unit"]).strip().upper() == "KG"
                  else pd.to_numeric(row["Qty"], errors="coerce")
              ),
              axis=1,
          )
          # Mengatur ulang posisi kolom agar Qty BB Standar (GR) tepat di sebelah kanan Qty
          cols = list(master_df.columns)
          if "Qty BB Standar (GR)" in cols and "Qty" in cols:
            cols.remove("Qty BB Standar (GR)")
            qty_idx = cols.index("Qty")
            cols.insert(qty_idx + 1, "Qty BB Standar (GR)")
            master_df = master_df[cols]
        else:
          master_df["Qty BB Standar (GR)"] = 0

        # Pastikan kolom teks tersedia
        if "Keterangan" not in master_df.columns:
          master_df["Keterangan"] = ""
        if "Keterangan Lain" not in master_df.columns:
          master_df["Keterangan Lain"] = ""
        if "Nama Barang Jadi" not in master_df.columns:
          master_df["Nama Barang Jadi"] = ""

        # Fungsi Algoritma Audit per Baris (menggunakan Kode Item dan Nama Item)
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

        for idx, row in master_df.iterrows():
          kode_trans = str(row.get("Kode", ""))
          gudang = str(row.get("Gudang", ""))
          kode_item = str(row.get("Kode Item", ""))
          nama_brg_jdi = str(row.get("Nama Barang Jadi", ""))
          ket = str(row.get("Keterangan", ""))
          ket_lain = str(row.get("Keterangan Lain", ""))

          if (
              not kode_trans
              or kode_trans == "nan"
              or not kode_item
              or kode_item == "nan"
          ):
            cek_jumlah_benang_list.append("")
            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            continue

          if gudang == "Gudang dyeing STI":
            cek_jumlah_benang_list.append("")
            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            continue

          sub_df = master_df[master_df["Kode"] == kode_trans]

          if gudang == "PRODUKSI SOFTCONE":
            benang_sub = sub_df[
                sub_df["Kode Item"]
                .astype(str)
                .str.startswith(("TBB", "MBB", "MWP", "TWP", "TBM"), na=False)
            ]
          else:
            benang_sub = sub_df[
                sub_df["Kode Item"]
                .astype(str)
                .str.startswith(("TWP", "MWP", "TBM"), na=False)
            ]

          if not benang_sub.empty:
            unique_benang = ", ".join(
                benang_sub["Kode Item"].astype(str).unique()
            )
            cek_jumlah_benang_list.append(unique_benang)
          else:
            cek_jumlah_benang_list.append("Tidak Ada TWP/MWP/TBM")

          first_idx_for_code = master_df[master_df["Kode"] == kode_trans].index[
              0
          ]
          if idx != first_idx_for_code:
            crosscheck_qty_list.append("")
            selisih_list.append("")
            satuan_selisih_list.append("")
            continue

          target_qty = round(
              float(
                  pd.to_numeric(
                      row.get("QTY Target Standar (GR)", 0), errors="coerce"
                  )
              ),
              0,
          )

          if gudang == "PRODUKSI SOFTCONE":
            total_bb = round(
                benang_sub[
                    benang_sub["Kode Item"]
                    .astype(str)
                    .str.startswith(("TBB", "MBB", "TWP", "TBM", "MWP"), na=False)
                ]["Qty BB Standar (GR)"].sum(),
                0,
            )
          elif gudang in ["Gudang mesin dyeing", "GUDANG LAB & RnD"]:
            total_bb = round(
                benang_sub[
                    benang_sub["Kode Item"]
                    .astype(str)
                    .str.startswith(("TWP", "MWP", "TBM"), na=False)
                ]["Qty BB Standar (GR)"].sum(),
                0,
            )
          else:
            total_bb = 0

          selisih_val = target_qty - total_bb
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
        st.success("✨ Proses validasi selesai dengan sukses!")

    # Tampilkan hasil & tombol download jika sudah diproses
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

      valid_status = processed_df["Crosscheck Qty"].replace("", pd.NA).dropna()
      total_trx = len(valid_status)
      correct_count = (valid_status == "CORRECT").sum()
      incorrect_normal = (valid_status == "INCORRECT").sum()
      incorrect_wajar = (
          valid_status == "INCORRECT (Memang Benar Selisih)"
      ).sum()

      m1, m2, m3, m4 = st.columns(4)
      with m1:
        st.metric(
            label="Total Kelompok Transaksi", value=f"{total_trx:,} Baris"
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
