import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def pilih_stack():
    print("==== Docker Setup Automator ====")
    print("1. Laravel & MySQL")
    print("2. NodeJS & MySQL")
    print("3. PHP & MySQL")
    choice=input("Pilih Stack (1/2/3) : ")
    return choice

def tanya_folder():
    folder=input("Masukkan lokasi folder project : ")
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"📂 Folder {folder} berhasil dibuat.")
    return folder

def copy_template(stack,target_folder):
    templates={
            "1":os.path.join(BASE_DIR,"templates/laravel"),
            "2":os.path.join(BASE_DIR,"templates/nodejs"),
            "3":os.path.join(BASE_DIR,"php-mysql")
            }
    if stack in templates:
        src = templates[stack]
        files = os.listdir(src)
        for f in files:
            shutil.copy(f"{src}/{f}",os.path.join(target_folder,f))
        print(f"✅ File berhasil di-generate di {target_folder}")
    else:
        print("❌ Pilihan Tidak valid")

if __name__=="__main__":
    stack=pilih_stack()
    target_folder=tanya_folder()
    copy_template(stack,target_folder)
