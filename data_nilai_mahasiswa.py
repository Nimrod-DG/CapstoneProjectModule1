from tabulate import tabulate

HEADERS = [
    "NIM", "Nama", "Gender", "Program", "Angkatan", 
    "Metode Belajar", "Jadwal", "Modul 1", "Modul 2", "Modul 3"
]

PROGRAM_LIST = [
    "Data Science & Machine Learning",
    "Business & Data Analyst",
    "Product Management",
    "Digital Marketing",
    "Fullstack Web Development",
    "Visual & UI/UX Design",
    "3D & Animation",
    "UI/UX & Front End Development"
]

GENDER_OPTIONS = {'1': "Laki - Laki", '2': "Perempuan"}
METHOD_OPTIONS = {'1': "Online", '2': "On Campus"}
SCHEDULE_OPTIONS = {'1': "Office Hours", '2': "After Hours"}


def validate_alpha_only(value):
    if not value.strip():
        return False
    if not value.replace(" ", "").isalpha():
        return False
    return True

def validate_not_empty(input_str):
    return input_str != ""

def validate_nim(input_str, existing_nims):
    return input_str and input_str.upper() not in existing_nims

def validate_digit_range(input_str, min_val, max_val):
    return input_str.isdigit() and min_val <= int(input_str) <= max_val

def validate_four_digits(input_str):
    return input_str.isdigit() and len(input_str) == 4

def validate_modul_score(input_str):
    return input_str.isdigit() and 0 <= int(input_str) <= 100

def validate_yes_no(input_str):
    return input_str.lower() in ['y', 'n']

def get_table_width(rows, headers=None, tablefmt="simple", colalign=None):
    if headers is None:
        headers = []
    if colalign is None:
        colalign = ['center'] * len(headers) if headers else []
    
    table_str = tabulate(rows, headers=headers, tablefmt=tablefmt, colalign=colalign)
    return max(len(line) for line in table_str.splitlines())

def display_menu(title, menu_items, header=("No.", "Pilihan")):
    menu_table = []
    for i, item in enumerate(menu_items, 1):
        menu_table.append([i, item])
    
    table_width = get_table_width(menu_table, headers=[header[0], header[1]], tablefmt="grid", colalign=("center", "center"))
    
    centered_title = f"===== {title} =====".center(table_width)
    
    print("\n" + centered_title)
    print(tabulate(menu_table, headers=[header[0], header[1]], tablefmt="grid", colalign=("center", "center")))
    print("=" * table_width)

def tampilkan_data(rows):
    if rows:
        table_width = get_table_width(rows, headers=HEADERS, tablefmt="grid", colalign=['center'] * len(HEADERS))
        print("\n" + "===== Data Mahasiswa =====".center(table_width))
        print(tabulate(rows, headers=HEADERS, tablefmt="grid", colalign=['center'] * len(HEADERS)))
    else:
        print("Data tidak ditemukan berdasarkan kriteria pencarian!")

def display_options(title, options):
    menu_table = []

    if isinstance(options, dict):
        for key, value in options.items():
            menu_table.append([key, value])
    else:
        for i, option in enumerate(options, 1):
            menu_table.append([i, option])

    headers = ["No.", "Deskripsi"]

    table_width = get_table_width(menu_table, headers=headers, tablefmt="grid", colalign=("center", "center"))

    centered_title = f"===== {title} =====".center(table_width)

    print("\n" + centered_title)
    print(tabulate(menu_table, headers=headers, tablefmt="grid", colalign=("center", "center")))
    print("=" * table_width)

def input_valid(prompt, validator, error_msg, existing_nims=None, min_val=None, max_val=None):
    while True:
        val = input(prompt).strip()
        if validator == validate_nim:
            if validate_nim(val, existing_nims):
                return val.upper()
        elif validator == validate_digit_range:
            if validate_digit_range(val, min_val, max_val):
                return val
        elif validator(val):
            return val
        print(f"{error_msg}!")

def input_pilihan(prompt, pilihan_dict):
    display_options(prompt, pilihan_dict)
    while True:
        pilih = input("Masukkan pilihan: ").strip()
        if pilih in pilihan_dict:
            return pilihan_dict[pilih]
        print("Pilihan tidak valid!")

def input_program(prompt):
    display_options("Pilihan Program", PROGRAM_LIST)
    return PROGRAM_LIST[int(input_valid(
        "Masukkan nomor program pilihan: ",
        validate_digit_range,
        f"Masukkan nomor 1 sampai {len(PROGRAM_LIST)}",
        min_val=1,
        max_val=len(PROGRAM_LIST)
    )) - 1]

def input_modul(nomor):
    return int(input_valid(
        f"Masukkan nilai Modul {nomor} (0-100): ",
        validate_modul_score,
        "Nilai modul harus angka antara 0 sampai 100"
    ))

def generate_rows(data_dict, nims):
    return [
        [
            nim,
            data_dict[nim]["nama"],
            data_dict[nim]["gender"],
            data_dict[nim]["program"],
            data_dict[nim]["angkatan"],
            data_dict[nim]["metode_belajar"],
            data_dict[nim]["jadwal"],
            data_dict[nim]["modul_1"],
            data_dict[nim]["modul_2"],
            data_dict[nim]["modul_3"]
        ] for nim in nims
    ]

def input_mahasiswa(data_mahasiswa):
    nim = input_valid(
        "Masukkan NIM (unik): ",
        validate_nim,
        "NIM tidak boleh kosong atau sudah ada",
        existing_nims=data_mahasiswa.keys()
    )

    nama = input_valid(
    "Masukkan Nama: ",
    validate_alpha_only,
    "Nama tidak boleh kosong dan hanya boleh berisi huruf"
)
    gender = input_pilihan("Pilih Gender:", GENDER_OPTIONS)
    program = input_program("")
    
    angkatan = int(input_valid(
        "Masukkan Angkatan (4 digit, contoh 2023): ",
        validate_four_digits,
        "Angkatan harus berupa angka 4 digit"
    ))

    metode_belajar = input_pilihan("Pilih Metode Belajar:", METHOD_OPTIONS)
    jadwal = input_pilihan("Pilih Jadwal:", SCHEDULE_OPTIONS)

    print("")
    modul_1 = input_modul(1)
    modul_2 = input_modul(2)
    modul_3 = input_modul(3)

    return {
        "nim": nim,
        "nama": nama,
        "gender": gender,
        "program": program,
        "angkatan": angkatan,
        "metode_belajar": metode_belajar,
        "jadwal": jadwal,
        "modul_1": modul_1,
        "modul_2": modul_2,
        "modul_3": modul_3
    }

def report_data(data_mahasiswa):
    kolom_dict = {
        '1': 'nim',
        '2': 'nama',
        '3': 'gender',
        '4': 'program',
        '5': 'angkatan',
        '6': 'metode_belajar',
        '7': 'jadwal'
    }

    while True:
        menu_items = [
            "Report Seluruh Data",
            "Report Data Tertentu",
            "Kembali Ke Menu Utama"
        ]
        display_menu("Menu Report Data Siswa", menu_items)
        pilihan = input("Silakan Pilih Sub Menu Read Data [1-3]: ").strip()

        if pilihan == '1':
            rows = generate_rows(data_mahasiswa, data_mahasiswa.keys())
            tampilkan_data(rows)

        elif pilihan == '2':
            kolom_options = {k: v.capitalize().replace('_', ' ') for k, v in kolom_dict.items()}
            display_options("Cari Berdasarkan", kolom_options)
            kolom_pilih = input("\nPilih kolom pencarian [1-7]: ").strip()

            if kolom_pilih not in kolom_dict:
                print("Pilihan kolom tidak valid!\n")
                continue

            kolom = kolom_dict[kolom_pilih]
            keyword = ""

            if kolom == 'nim' or kolom == 'nama':
                keyword = input("Masukkan kata kunci pencarian: ").replace(" ", "").lower()
            
            elif kolom == 'gender':
                keyword = input_pilihan("Pilih Gender:", GENDER_OPTIONS)
                keyword = keyword.replace(" ", "").lower()
            
            elif kolom == 'program':
                keyword = input_program("")
                keyword = keyword.replace(" ", "").lower()
            
            elif kolom == 'angkatan':
                keyword = input_valid("Masukkan Angkatan (4 digit): ",
                                      validate_four_digits,
                                      "Angkatan harus berupa angka 4 digit")
            
            elif kolom == 'metode_belajar':
                keyword = input_pilihan("Pilih Metode Belajar:", METHOD_OPTIONS)
                keyword = keyword.replace(" ", "").lower()
            
            elif kolom == 'jadwal':
                keyword = input_pilihan("Pilih Jadwal:", SCHEDULE_OPTIONS)
                keyword = keyword.replace(" ", "").lower()

            hasil_nim = []
            for nim, data in data_mahasiswa.items():
                if kolom == 'nim':
                    nilai_cari = nim
                elif kolom == 'program':
                    nilai_cari = data["program"]
                elif kolom == 'angkatan':
                    nilai_cari = str(data["angkatan"])
                else:
                    nilai_cari = str(data.get(kolom, ""))
    
                nilai_cari = nilai_cari.replace(" ", "").lower()
                
                if keyword in nilai_cari:
                    hasil_nim.append(nim)
            rows = generate_rows(data_mahasiswa, hasil_nim)
            tampilkan_data(rows)

        elif pilihan == '3':
            print(">> Kembali ke menu utama...\n")
            return
        else:
            print("Input tidak valid! Silakan masukkan angka 1 hingga 3.\n")

def add_data(data_mahasiswa):
    while True:
        menu_items = [
            "Tambah Data",
            "Kembali ke Menu Utama"
        ]
        display_menu("Menu Add Data Siswa", menu_items)
        pilihan = input("Masukkan pilihan [1-2]: ").strip()

        if pilihan == '1':
            print("\n>> Menambahkan Data Siswa...\n")
            data = input_mahasiswa(data_mahasiswa)
            
            rows = generate_rows({data["nim"]: data}, [data["nim"]])
            tampilkan_data(rows)
            print("")
            if input_valid("Konfirmasi tambah data? (Y/N): ",
                           validate_yes_no,
                           "Masukkan Y untuk Ya atau N untuk Tidak").lower() == 'y':
                data_mahasiswa[data["nim"]] = data
                print(f"\nData mahasiswa dengan NIM {data['nim']} berhasil ditambahkan.\n")
            else:
                print("\nPenambahan data dibatalkan.\n")

        elif pilihan == '2':
            print(">> Kembali ke menu utama...\n")
            return
        else:
            print("Pilihan tidak valid! Masukkan angka 1 atau 2.\n")

def update_data(data_mahasiswa):
    while True:
        menu_items = [
            "Ubah Data Mahasiswa",
            "Kembali ke Menu Utama"
        ]
        display_menu("Menu Update Data Siswa", menu_items)
        choice = input("Masukkan pilihan [1-2]: ").strip()

        if choice == '2':
            print(">> Kembali ke menu utama...\n")
            return

        if choice != '1':
            print("Pilihan tidak valid! Masukkan angka 1 atau 2.\n")
            continue

        nim = input("Masukkan NIM mahasiswa yang ingin diubah: ").upper().strip()
        if nim not in data_mahasiswa:
            print(f"\nData dengan NIM {nim} tidak ditemukan!")
            continue

        student_data = data_mahasiswa[nim]
        rows = generate_rows(data_mahasiswa, [nim])
        tampilkan_data(rows)
        if input_valid("\nLanjutkan perubahan? (Y/N): ",
                       validate_yes_no,
                       "Masukkan Y untuk Ya atau N untuk Tidak").lower() != 'y':
            print(">> Pengubahan data dibatalkan.\n")
            continue

        print("\nPilih kolom yang ingin diubah:")
        kolom_options = {
            '1': ('Nama', 'nama'),
            '2': ('Gender', 'gender'),
            '3': ('Program', 'program'),
            '4': ('Angkatan', 'angkatan'),
            '5': ('Metode Belajar', 'metode_belajar'),
            '6': ('Jadwal', 'jadwal'),
            '7': ('Modul 1', 'modul_1'),
            '8': ('Modul 2', 'modul_2'),
            '9': ('Modul 3', 'modul_3')
        }
        display_options("Pilihan Kolom", [v[0] for v in kolom_options.values()])
        kolom_choice = input("\nMasukkan nomor kolom: ").strip()
        if kolom_choice not in kolom_options:
            print("Pilihan tidak valid!\n")
            continue

        kolom_name, kolom_key = kolom_options[kolom_choice]
        print(f"\nMengubah {kolom_name}...")

        if kolom_key == 'nama':
            new_value = input_valid("Masukkan Nama baru: ", validate_not_empty, "Nama tidak boleh kosong")
        elif kolom_key == 'gender':
            new_value = input_pilihan("Pilih Gender baru:", GENDER_OPTIONS)
        elif kolom_key == 'program':
            new_value = input_program("")
        elif kolom_key == 'angkatan':
            new_value = int(input_valid("Masukkan Angkatan baru (4 digit): ",
                                        validate_four_digits,
                                        "Angkatan harus berupa angka 4 digit"))
        elif kolom_key == 'metode_belajar':
            new_value = input_pilihan("Pilih Metode Belajar baru:", METHOD_OPTIONS)
        elif kolom_key == 'jadwal':
            new_value = input_pilihan("Pilih Jadwal baru:", SCHEDULE_OPTIONS)
        else: 
            new_value = input_modul(kolom_name.split()[-1])

        if input_valid(f"Konfirmasi ubah {kolom_name} menjadi '{new_value}'? (Y/N): ",
                       validate_yes_no,
                       "Masukkan Y untuk Ya atau N untuk Tidak").lower() == 'y':
            student_data[kolom_key] = new_value
            print(f"\n>> Data {kolom_name} untuk NIM {nim} berhasil diperbarui.")
            rows = generate_rows(data_mahasiswa, [nim])
            tampilkan_data(rows)
        else:
            print(">> Perubahan dibatalkan.\n")

def delete_data(data_mahasiswa):
    while True:
        menu_items = [
            "Hapus berdasarkan NIM",
            "Hapus berdasarkan Nama",
            "Hapus berdasarkan Kriteria",
            "Kembali ke menu utama"
        ]
        display_menu("Menu Hapus Data Siswa", menu_items)
        choice = input("Pilih opsi [1-4]: ").strip()

        if choice == '4':
            print(">> Kembali ke menu utama...\n")
            return

        if choice not in ['1', '2', '3']:
            print("Pilihan tidak valid! Masukkan angka 1 hingga 4.\n")
            continue

        if choice == '1':
            nim = input("Masukkan NIM mahasiswa: ").upper().strip()
            if nim not in data_mahasiswa:
                print(f"Data dengan NIM {nim} tidak ditemukan!\n")
                continue
            
            rows = generate_rows(data_mahasiswa, [nim])
            tampilkan_data(rows)

            if input_valid("\nKonfirmasi hapus data ini? (Y/N): ",
                           validate_yes_no,
                           "Masukkan Y untuk Ya atau N untuk Tidak").lower() == 'y':
                del data_mahasiswa[nim]
                print(f">> Data dengan NIM {nim} berhasil dihapus.\n")
            else:
                print(">> Penghapusan dibatalkan.\n")

        elif choice == '2':
            name = input("Masukkan nama mahasiswa: ").strip().lower()
            matches = []
            for nim, data in data_mahasiswa.items():
                if name == data['nama'].lower():
                    matches.append(nim)

            if not matches:
                print(f"Data dengan Nama {name} tidak ditemukan!\n")
                continue
            
            rows = generate_rows(data_mahasiswa, matches)
            tampilkan_data(rows)

            if len(matches) == 1:
                nim_to_del = matches[0]
            else:
                nim_to_del = input("\nMasukkan NIM mahasiswa yang ingin dihapus: ").upper().strip()
                if nim_to_del not in matches:
                    print("NIM tidak valid atau tidak ada dalam daftar yang ditemukan!\n")
                    continue

            if input_valid("\nKonfirmasi hapus data ini? (Y/N): ", validate_yes_no, "Masukkan Y atau N").lower() == 'y':
                del data_mahasiswa[nim_to_del]
                print(f"\n>> Data dengan NIM {nim_to_del} berhasil dihapus.\n")
            else:
                print(">> Penghapusan dibatalkan.\n")

        else:  
            kriteria_options = {
                '1': "Gender",
                '2': "Program",
                '3': "Angkatan",
                '4': "Metode Belajar",
                '5': "Jadwal"
            }
            display_options("Kriteria Penghapusan", kriteria_options)
            kriteria_choice = input("\nMasukkan nomor kriteria: ").strip()
            if kriteria_choice not in kriteria_options:
                print("Pilihan tidak valid! Masukkan anggka 1 hingga 5.\n")
                continue

            kriteria_name = kriteria_options[kriteria_choice]
            key_map = {
                "Gender": 'gender',
                "Program": 'program',
                "Angkatan": 'angkatan',
                "Metode Belajar": 'metode_belajar',
                "Jadwal": 'jadwal'
            }
            key = key_map[kriteria_name]

            if kriteria_name == "Gender":
                value = input_pilihan(f"Pilih {kriteria_name}:", GENDER_OPTIONS)
            elif kriteria_name == "Program":
                value = input_program(f"Masukkan nomor {kriteria_name}: ")
            elif kriteria_name == "Angkatan":
                value = int(input_valid(f"Masukkan {kriteria_name} (4 digit): ",
                                        validate_four_digits,
                                        "Harus angka 4 digit"))
            elif kriteria_name == "Metode Belajar":
                value = input_pilihan(f"Pilih {kriteria_name}:", METHOD_OPTIONS)
            else:
                value = input_pilihan(f"Pilih {kriteria_name}:", SCHEDULE_OPTIONS)

            to_delete = []
            for nim, data in data_mahasiswa.items():
                if data[key] == value:
                    to_delete.append(nim)

            if not to_delete:
                print(f"\nTidak ditemukan data dengan {kriteria_name} = '{value}'!\n")
                continue

            print(f"\nDitemukan {len(to_delete)} data dengan {kriteria_name} = '{value}':")
            rows = generate_rows(data_mahasiswa, to_delete)
            tampilkan_data(rows)

            if input_valid("\nKonfirmasi hapus semua data di atas? (Y/N): ",
                           validate_yes_no,
                           "Masukkan Y untuk Ya atau N untuk Tidak").lower() == 'y':
                for nim in to_delete:
                    del data_mahasiswa[nim]
                print(f">> {len(to_delete)} data berhasil dihapus.\n")
            else:
                print(">> Penghapusan dibatalkan.\n")

def main_menu():
    data_mahasiswa = {
        "MH001": {
            "nama": "Andi Wijaya", "gender": "Laki - Laki", "program": "Data Science & Machine Learning",
            "angkatan": 2021, "metode_belajar": "Online", "jadwal": "After Hours",
            "modul_1": 85, "modul_2": 90, "modul_3": 88
        },
        "MH002": {
            "nama": "Budi Sutresno", "gender": "Laki - Laki", "program": "Business & Data Analyst",
            "angkatan": 2022, "metode_belajar": "On Campus", "jadwal": "Office Hours",
            "modul_1": 78, "modul_2": 80, "modul_3": 75
        },
        "MH003": {
            "nama": "Citra Hati", "gender": "Perempuan", "program": "Product Management",
            "angkatan": 2020, "metode_belajar": "Online", "jadwal": "After Hours",
            "modul_1": 88, "modul_2": 92, "modul_3": 90
        },
        "MH004": {
            "nama": "Dewi Pertiwi", "gender": "Perempuan", "program": "Digital Marketing",
            "angkatan": 2023, "metode_belajar": "On Campus", "jadwal": "Office Hours",
            "modul_1": 70, "modul_2": 72, "modul_3": 68
        },
        "MH005": {
            "nama": "Eka Gunting", "gender": "Laki - Laki", "program": "Fullstack Web Development",
            "angkatan": 2024, "metode_belajar": "Online", "jadwal": "After Hours",
            "modul_1": 90, "modul_2": 85, "modul_3": 87
        },
        "MH006": {
            "nama": "Fajar Baru", "gender": "Laki - Laki", "program": "Visual & UI/UX Design",
            "angkatan": 2021, "metode_belajar": "On Campus", "jadwal": "Office Hours",
            "modul_1": 60, "modul_2": 65, "modul_3": 70
        },
        "MH007": {
            "nama": "Gita Bandung", "gender": "Perempuan", "program": "3D & Animation",
            "angkatan": 2025, "metode_belajar": "Online", "jadwal": "After Hours",
            "modul_1": 95, "modul_2": 93, "modul_3": 97
        },
        "MH008": {
            "nama": "Hari Pustaka", "gender": "Laki - Laki", "program": "UI/UX & Front End Development",
            "angkatan": 2022, "metode_belajar": "On Campus", "jadwal": "Office Hours",
            "modul_1": 75, "modul_2": 78, "modul_3": 74
        },
        "MH009": {
            "nama": "Indah Wijaya", "gender": "Perempuan", "program": "Digital Marketing",
            "angkatan": 2020, "metode_belajar": "Online", "jadwal": "After Hours",
            "modul_1": 82, "modul_2": 88, "modul_3": 85
        },
        "MH010": {
            "nama": "Joko Widodo", "gender": "Laki - Laki", "program": "Business & Data Analyst",
            "angkatan": 2023, "metode_belajar": "On Campus", "jadwal": "Office Hours",
            "modul_1": 68, "modul_2": 70, "modul_3": 65
        }
    }

    while True:
        menu_items = [
            "Report Data Siswa",
            "Menambahkan Data Siswa",
            "Mengubah Data Siswa",
            "Menghapus Data Siswa",
            "Exit"
        ]
        display_menu("Data Record Siswa Purwadhika", menu_items)
        pilihan = input("Silakan Pilih Main_Menu [1-5] : ")

        if pilihan == '1':
            report_data(data_mahasiswa)
        elif pilihan == '2':
            add_data(data_mahasiswa)
        elif pilihan == '3':
            update_data(data_mahasiswa)
        elif pilihan == '4':
            delete_data(data_mahasiswa)
        elif pilihan == '5':
            print(">> Keluar dari program. Terima kasih!")
            break
        else:
            print("Input tidak valid! Silakan masukkan angka antara 1 hingga 5.\n")

if __name__ == "__main__":
    main_menu()
