
#==========================================================================|
#|                       | MODEL PROGRAM CAR_RENTAL |                      |
#==========================================================================|
#                               PENJELASAN MODEL
#==========================================================================|
#  Dokumentasi Sistem Manajemen Unit Kendaraan Terintegrasi (CAR_RENTAL)
#  Sistem ini dirancang sebagai solusi digital bagi Administrator untuk 
#  mengoptimalkan efisiensi operasional harian pada perusahaan rental mobil. 
#  Fokus utama platform ini adalah integrasi data unit kendaraan, manajemen 
#  basis data pelanggan, serta otomatisasi kalkulasi transaksi penyewaan.
#==================================================================================================
#  1. PENGGUNAAN FITUR READ UNTUK USER (ADMIN) di CAR_RENTAL
#  Fitur ini berperan sebagai instrumen transparansi data bagi administrator.
#  Melalui modul ini, pengguna dapat memantau ketersediaan unit kendaraan secara real-time. 
# Keunggulan modul ini adalah kemampuannya menyajikan rincian spesifikasi setiap unit serta tarif 
# sewa harian yang akurat, sehingga mempermudah administrator dalam memberikan respon cepat terhadap 
# permintaan calon penyewa.
#=========================================================================================================
#  2. PENGGUNAAN FITUR CREATE UNTUK USER/ADMIN CAR_RENTAL DALAM Modul REGISTRASI UNIT KENDARAAN BARU
#   Digunakan sebagai pintu masuk data untuk setiap penambahan aset kendaraan baru perusahaan. 
#   Administrator memiliki wewenang penuh untuk meregistrasikan identitas teknis kendaraan secara mendetail, 
#   yang mencakup identitas unik (ID Mobil), nomor registrasi polisi (plat nomor), klasifikasi merek dan model, 
#   hingga penentuan tarif sewa serta penetapan status awal unit dalam sistem.
#==========================================================================================================
#  3. Modul Sinkronisasi Status & Pemeliharaan Data (Update/Edit)
#   Modul ini merupakan inti dari integritas data operasional. Peran utamanya 
#   adalah melakukan sinkronisasi status kendaraan berdasarkan aktivitas di lapangan. 
#   Fungsi ini memastikan bahwa setiap unit yang sedang dalam masa sewa akan secara otomatis 
#   diperbarui statusnya dari "Tersedia" menjadi "Sedang Disewa", guna mencegah risiko tumpang 
#   tindih pesanan (double booking).
#==============================================================================================================
#  4. Modul Manajemen Siklus Hidup Aset (Delete)
# Fitur ini dialokasikan untuk tata kelola inventaris jangka panjang. Administrator dapat melakukan penghapusan data 
# secara permanen apabila sebuah unit kendaraan sudah mencapai akhir masa pakai, mengalami kerusakan total, atau telah 
# dialihkan kepemilikannya (dijual), sehingga data pada laporan operasional tetap relevan.
#======================================================================================================================
# 5. Modul Transaksi & Manajemen Hubungan Pelanggan (Customer & Transaction)
#Fitur ini mengonsolidasikan interaksi antara administrator dan penyewa melalui alur kerja yang sistematis:
# Profil Pelanggan: Validasi dan digitalisasi identitas pribadi penyewa ke dalam basis data perusahaan.
#Otomatisasi Kalkulasi: Sistem akan memproses pemilihan unit kendaraan dan durasi sewa untuk menghasilkan 
# nilai transaksi secara otomatis, guna menciptakan transparansi biaya sebelum penyerahan kunci kendaraan


# --- DATABASE ---
data_mobil = [
    {"MobilID": 101, "PlatNomor": "B 1234 XY", "Merek": "Toyota", "Model": "Avanza", "Tahun": 2023, "Harga": 350000, "Status": "Tersedia"},
    {"MobilID": 102, "PlatNomor": "D 5678 AB", "Merek": "Honda", "Model": "Brio Satya", "Tahun": 2022, "Harga": 280000, "Status": "Sedang Disewa"},
    {"MobilID": 103, "PlatNomor": "A 9012 CD", "Merek": "Daihatsu", "Model": "Xenia", "Tahun": 2024, "Harga": 370000, "Status": "Tersedia"},
    {"MobilID": 104, "PlatNomor": "F 3456 EF", "Merek": "Suzuki", "Model": "Ertiga", "Tahun": 2021, "Harga": 300000, "Status": "Tersedia"},
    {"MobilID": 105, "PlatNomor": "B 7890 GH", "Merek": "Mitsubishi", "Model": "Xpander", "Tahun": 2023, "Harga": 400000, "Status": "Sedang Disewa"},
    {"MobilID": 106, "PlatNomor": "L 1122 IJ", "Merek": "Toyota", "Model": "Innova Reborn", "Tahun": 2020, "Harga": 550000, "Status": "Tersedia"},
]

data_pelanggan = [
    {"PelangganID": 1, "Nama": "Budi Santoso", "Telepon": "081234567890"},
    {"PelangganID": 2, "Nama": "Sari Dewi", "Telepon": "087654321098"},
    {"PelangganID": 3, "Nama": "Riko Adrian", "Telepon": "085712345678"},
    {"PelangganID": 4, "Nama": "Lia Fitriani", "Telepon": "082198765432"},
    {"PelangganID": 5, "Nama": "Taufik Hidayat", "Telepon": "089901122334"},
    {"PelangganID": 6, "Nama": "Citra Lestari", "Telepon": "081155667788"},
]

# --- FUNGSI PENCARIAN ---
def cari_data(daftar, kunci, target):
    for item in daftar:
        if item[kunci] == target:
            return item
    return None

# --- FUNGSI TAMPILAN TABEL ---
def cetak_tabel_mobil(daftar, judul):
    print(f"\n=== {judul.upper()} ===")
    print("-" * 85)
    print(f"{'ID':<5} | {'Plat':<12} | {'Merek':<12} | {'Model':<15} | {'Harga/Hari':<12} | {'Status'}")
    print("-" * 85)
    for m in daftar:
        print(f"{m['MobilID']:<5} | {m['PlatNomor']:<12} | {m['Merek']:<12} | {m['Model']:<15} | {m['Harga']:<12,} | {m['Status']}")
    print("-" * 85)

# --- PENGGUNAAN CRUD ---

def menu_lihat(): # ALUR READ
    while True:
        print("\n--- [1] MENU LAPORAN DATA ---")
        print("1. Tampilkan Semua Mobil\n2. Cari Mobil Spesifik\n3. Kembali")
        pilih = input("Pilih: ")
        if pilih == '1':
            cetak_tabel_mobil(data_mobil, "Daftar Seluruh Mobil")
        elif pilih == '2':
            tid = int(input("Masukkan MobilID: "))
            hasil = cari_data(data_mobil, "MobilID", tid)
            print(f"\nHasil: {hasil}" if hasil else "\n[!] Data does not exist")
        elif pilih == '3': break

def menu_tambah(): # ALUR CREATE
    while True:
        print("\n--- [2] MENU TAMBAH DATA ---")
        print("1. Tambah Mobil\n2. Kembali")
        if input("Pilih: ") == '1':
            new_id = int(input("Masukkan ID Baru: "))
            if cari_data(data_mobil, "MobilID", new_id):
                print("[!] Data already exists")
            else:
                platnomor = (input("PlatNomor: "))
                merek = input("Merek: ")
                model = input("Model: ")
                harga = int(input("Harga: "))
                status = input("Status: ")
                if input("Simpan data? (y/n): ").lower() == 'y':
                    data_mobil.append({"MobilID": new_id, "PlatNomor": platnomor, "Merek": merek, "Model": model, "Harga": harga, "Status": status})
                    print("[V] Data successfully saved")
        else: break

def menu_ubah(): # ALUR UPDATE
    while True:
        print("\n--- [3] MENU UBAH DATA ---")
        print("1. Edit Mobil\n2. Kembali")
        if input("Pilih: ") == '1':
            uid = int(input("Masukkan ID: "))
            mobil = cari_data(data_mobil, "MobilID", uid)
            if not mobil:
                print("[!] The data you are looking for does not exist")
            else:
                print(f"Data: {mobil}")
                if input("Lanjut Ubah? (y/n): ").lower() == 'y':
                    kolom = input("Kolom yang diubah (Merek/Harga/Status): ")
                    if kolom in mobil:
                        mobil[kolom] = input("Nilai Baru: ")
                        print("[V] Data successfully updated")
        else: break

def menu_hapus(): # ALUR DELETE
    while True:
        print("\n--- [4] MENU HAPUS DATA ---")
        print("1. Hapus Mobil\n2. Kembali")
        if input("Pilih: ") == '1':
            did = int(input("Masukkan ID: "))
            mobil = cari_data(data_mobil, "MobilID", did)
            if not mobil:
                print("[!] The data you are looking for does not exist")
            else:
                if input(f"Hapus ID {did}? (y/n): ").lower() == 'y':
                    data_mobil.remove(mobil)
                    print("[V] Data successfully deleted")
        else: break

def menu_transaksi(): # ALUR TAMBAHAN TRANSAKSI
    print("\n--- [5] MENU TRANSAKSI SEWA ---")
    pid = int(input("Masukkan PelangganID: "))
    pelanggan = cari_data(data_pelanggan, "PelangganID", pid)
    if not pelanggan:
        print("[!] Pelanggan tidak terdaftar")
        return
    
    ready = [m for m in data_mobil if m["Status"] == "Tersedia"]
    cetak_tabel_mobil(ready, "Mobil Tersedia")
    
    mid = int(input("Pilih MobilID: "))
    mobil = cari_data(data_mobil, "MobilID", mid)
    if mobil and mobil["Status"] == "Tersedia":
        hari = int(input("Lama Sewa (Hari): "))
        total = hari * mobil["Harga"]
        print(f"Total Bayar: Rp {total:,}")
        if input("Konfirmasi? (y/n): ").lower() == 'y':
            mobil["Status"] = "Sedang Disewa"
            print("[V] Transaksi Berhasil!")

# --- MAIN LOOP (Halaman 1 Flowchart) ---
while True:
    print("\n" + "="*40)
    print("   RENTAL CAR MANAGEMENT SYSTEM   ")
    print("="*40)
    print("1. Report Data\n2. Add Data\n3. Edit Data\n4. Delete Data\n5. Transaksi Sewa\n6. Exit")
    opsi = input("Pilih Menu Utama: ")

    if opsi == '1': menu_lihat()
    elif opsi == '2': menu_tambah()
    elif opsi == '3': menu_ubah()
    elif opsi == '4': menu_hapus()
    elif opsi == '5': menu_transaksi()
    elif opsi == '6': break
    else: print("[!] The option you entered is not valid")


#                               MODEL PEMOGRAMAMAN CAR_RENTAL

#PROGARAM DIBUAT UNTUK ADMIN SEBAGAI USER PROGRAM YANG DIBUAT OLEH PERUSAHAAN RENTAL.

#1.Pada fitur READ, penggunaan fitur READ untuk admin CAR_RENTAL adalah untuk mengecek status ketersediaan mobil yang akan dirental
#   TUJUAN PROGRAM INI DIBUAAT ADALAH SAAT USER MENCARI MOBIL MANA YANG TERSEDIA BESERTA HARGA RENTAL 
#   MOBIL PER HARINYA

#2. Pada fitur ADD data, admin menggunakan fitur ini untuk mobil baru yang baru masuk di perusahaan CAR_RENTAL 
#   fungsi fitur ini juga untuk menginput mobil baru beserta iDMobil, Platnomor, Merek, Model, Harga, dan Satutsnya.

#3. Penggunaan fitur EDIT untuk admin CAR_RENTAL adalah jika admin ingin mengganti status 
#   jika mobil sedang disewa sehingga untuk merubah status dari mobil yang tersedia menjadi tidak tersedia

#4. Fitur DELETE untuk user atau admin digunakan saat mobil tidak akan digunakan lagi di perusaahan CAR_RENTAL

#5. fitur transaksi customer diminta untuk memasukan data pribadi, admin menginput data pribadi customer.
#saat  customer siap merental mobil sesuai pesanan yang diinginkan, admin menggunakan program car_rent
#dengan memilih mobil yang diinginkan customer, lalu ditotalkan hargany berdasarkann lama sewanya.
