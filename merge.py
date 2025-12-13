import pandas as pd
import glob

# Path ke folder berisi CSV
path = path = "XXXXXXXXXXXXXXXX"

# Ambil semua file CSV
all_files = glob.glob(path)

# Baca dan gabungkan semua CSV
df_list = [pd.read_csv(file) for file in all_files]
df_final = pd.concat(df_list, ignore_index=True)

# Simpan ke satu file CSV
df_final.to_csv("hasil_gabungan.csv", index=False)

print("CSV berhasil digabung menjadi hasil_gabungan.csv")
