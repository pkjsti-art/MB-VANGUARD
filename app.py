import io
import pandas as pd
import streamlit as st

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="MB-VANGUARD | Audit Data Manufacture Basic",
    page_icon="⚡",
    layout="wide",
)

# Custom Styling CSS (Tema Terang Cerah: Blue Sky, Putih, Hitam, Kuning Futuristik)
st.markdown(
    """
    <style>
    /* Global Styling */
    .stApp {
        background-color: #F0F8FF; /* Alice Blue / Soft Blue Sky */
        color: #111111;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header Utama */
    .main-header {
        background: linear-gradient(135deg, #00B4DB 0%, #0083B0 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 180, 219, 0.3);
        margin-bottom: 25px;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .main-header p {
        margin: 5px 0 0 0;
        font-size: 1.05rem;
        opacity: 0.9;
    }

    /* Container Kartu / Box */
    .metric-card {
        background-color: #FFFFFF;
        border: 2px solid #E1E8ED;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Tombol Kustom dengan Aksen Kuning Futuristik */
    div.stButton > button {
        background-color: #FFD700; /* Kuning Cerah */
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

    /* Styling Tabel & Dataframe */
    dataframe {
        border-radius: 8px;
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

# Instruksi & Upload File Multi-Gudang
st.markdown(
    "### 📂 1. Unggah File Master Export ERP Gudang"
)
uploaded_files = st.file_uploader(
    "Pilih atau geser file Excel master gudang Anda secara bersamaan (.xlsx)",
    type=["xlsx"],
    accept_multiple_files=True,
)

if uploaded_files:
  all_dataframes = []

  # Proses membaca setiap file yang di-upload
  for file in uploaded_files:
    try:
      df_raw = pd.read_excel(file)
      all_dataframes.append(df_raw)
    except Exception as e:
      st.error(f"Gagal membaca file {file.name}: {e}")

  if all_dataframes:
    # Gabungkan semua data dari berbagai gudang
    master_df = pd.concat(all_dataframes, ignore_index=True)

    # 1. Forward Fill untuk kolom identitas yang kosong ke bawah
    fill_cols = ["Gudang", "Kode", "Status", "Kode Barang Jadi", "Nama Barang Jadi"]
    for col in fill_cols:
      if col in master_df.columns:
        master_df[col] = master_df[col].ffill()

    # 2. Standarisasi Qty Target Standar (GR)
    if "Target Qty" in master_df.columns and "Target Unit" in master_df.columns:
      master_df["QTY Target Standar (GR)"] = master_df.apply(
          lambda row: (
              row["Target Qty"] * 1000
              if str(row["Target Unit"]).strip().upper() == "KG"
              else row["Target Qty"]
          ),
          axis=1,
      )
    else:
      master_df["QTY Target Standar (GR)"] = 0

    # 3. Standarisasi Qty Bahan Baku Standar (GR)
    if "Qty" in master_df.columns and "Unit" in master_df.columns:
      master_df["Qty BB Standar (GR)"] = master_df.apply(
          lambda row: (
              row["Qty"] * 1000
              if str(row["Unit"]).strip().upper() == "KG"
              else row["Qty"]
          ),
          axis=1,
      )
    else:
      master_df["Qty BB Standar (GR)"] = 0

    # Pastikan kolom tambahan penunjang audit tersedia
    if "Keterangan" not in master_df.columns:
      master_df["Keterangan"] = ""
    if "Keterangan Lain" not in master_df.columns:
      master_df["Keterangan Lain"] = ""

    # Proses Perhitungan per Baris Transaksi
    # Untuk efisiensi Python, kita buat fungsi kalkulasi bantu
    def process_audit_row(df):
      cek_jumlah_benang_list = []
      crosscheck_qty_list = []
      selisih_list = []
      satuan_selisih_list = []

      # List kata kunci pengecualian (case-insensitive)
      keywords = [
          "AVALAN",
          "CROCHET",
          "KOR",
          "KOR ROMBE",
          "KOLONG",
          "REEBOK",
          "ROLL",
      ]

      for idx, row in df.iterrows():
        kode_trans = str(row.get("Kode", ""))
        gudang = str(row.get("Gudang", ""))
        kode_bb = str(row.get("Kode Bahan Baku", ""))
        nama_brg_jdi = str(row.get("Nama Barang Jadi", ""))
        ket = str(row.get("Keterangan", ""))
        ket_lain = str(row.get("Keterangan Lain", ""))

        # Cek apakah baris kosong / invalid
        if not kode_trans or kode_trans == "nan" or not kode_bb or kode_bb == "nan":
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

        # Ambil subset dataframe untuk kode transaksi yang sama
        sub_df = df[df["Kode"] == kode_trans]

        # A. Cek Jumlah Benang
        if gudang == "PRODUKSI SOFTCONE":
          benang_sub = sub_df[
              sub_df["Kode Bahan Baku"]
              .str.startswith(("TBB", "MBB", "MWP", "TWP", "TBM"), na=False)
          ]
        else:  # Gudang mesin dyeing, Gudang Lab & RnD, dll
          benang_sub = sub_df[
              sub_df["Kode Bahan Baku"].str.startswith(("TWP", "MWP", "TBM"), na=False)
          ]

        if not benang_sub.empty:
          unique_benang = ", ".join(benang_sub["Kode Bahan Baku"].unique())
          cek_jumlah_benang_list.append(unique_benang)
        else:
          cek_jumlah_benang_list.append("Tidak Ada TWP/MWP/TBM")

        # Cek apakah ini baris utama (ambil baris pertama dari kelompok kode transaksi yang sama)
        first_idx_for_code = df[df["Kode"] == kode_trans].index[0]

        if idx != first_idx_for_code:
          # Baris duplikat di bawahnya dikosongkan untuk crosscheck & selisih agar rapi
          crosscheck_qty_list.append("")
          selisih_list.append("")
          satuan_selisih_list.append("")
          continue

        # B. Crosscheck Qty & Perhitungan Selisih
        target_qty = round(float(row.get("QTY Target Standar (GR)", 0)), 0)

        if gudang == "PRODUKSI SOFTCONE":
          total_bb = round(
              benang_sub[
                  benang_sub["Kode Bahan Baku"].str.startswith(
                      ("TBB", "MBB", "TWP", "TBM", "MWP"), na=False
                  )
              ]["Qty BB Standar (GR)"].sum(),
              0,
          )
        elif gudang in ["Gudang mesin dyeing", "GUDANG LAB & RnD"]:
          total_bb = round(
              benang_sub[
                  benang_sub["Kode Bahan Baku"].str.startswith(
                      ("TWP", "MWP", "TBM"), na=False
                  )
              ]["Qty BB Standar (GR)"].sum(),
              0,
          )
        else:
          total_bb = 0

        selisih_val = target_qty - total_bb

        # Deteksi kata kunci pengecualian di Nama Barang Jadi / Keterangan / Keterangan Lain
        combined_text = f"{nama_brg_jdi} {ket} {ket_lain}".upper()
        has_keyword = any(kw in combined_text for kw in keywords)

        if target_qty == total_bb:
          crosscheck_qty_list.append("CORRECT")
          selisih_list.append(selisih_val if selisih_val != 0 else 0)
          satuan_selisih_list.append("GR" if selisih_val != 0 else "GR")
        else:
          if has_keyword:
            crosscheck_qty_list.append("INCORRECT (Memang Benar Selisih)")
          else:
            crosscheck_qty_list.append("INCORRECT")
          selisih_list.append(selisih_val)
          satuan_selisih_list.append("GR")

      df["Cek jumlah benang"] = cek_jumlah_benang_list
      df["Crosscheck Qty"] = crosscheck_qty_list
      df["Selisih"] = selisih_list
      df["Satuan Selisih"] = satuan_selisih_list
      return df

    # Jalankan proses audit otomatis
    processed_df = process_audit_row(master_df)

    st.success("✅ Seluruh file gudang berhasil digabungkan dan divalidasi!")

    # --- TOMBOL DOWNLOAD DI ATAS TABEL ---
    st.markdown("---")
    col_dl1, col_dl2 = st.columns([2, 1])
    with col_dl1:
      st.markdown("### 📊 Ringkasan Hasil & Preview Data")
    with col_dl2:
      # Ubah DataFrame menjadi file Excel di memori untuk di-download
      output_buffer = io.BytesIO()
      with pd.ExcelWriter(output_buffer, engine="openpyxl") as writer:
        processed_df.to_excel(writer, index=False, sheet_name="Master_Validasi")
      excel_data = output_buffer.getvalue()

      st.download_button(
          label="📥 Download Laporan Excel (.xlsx)",
          data=excel_data,
          file_name="Laporan_Master_Validasi_MB.xlsx",
          mime=(
              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          ),
      )

    # Menampilkan Metrik Ringkasan Status
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

    # Filter Interaktif Berdasarkan Status
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
      display_df = processed_df[processed_df["Crosscheck Qty"] == status_filter]
    else:
      display_df = processed_df

    # Preview Tabel Bersih & Rapi
    st.dataframe(display_df, use_container_width=True, height=450)

  else:
    st.warning("⚠️ File yang di-upload kosong atau format tidak valid.")
else:
  st.info(
      "💡 Silakan upload file master ERP gudang Anda di atas untuk memulai"
      " proses otomatisasi MB-VANGUARD."
  )
