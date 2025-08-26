
---

## 📄 README untuk **Docker Setup Automator**

```markdown
# 🐳 Docker Setup Automator

Docker Setup Automator adalah script Python untuk membuat **docker-compose setup** secara otomatis untuk berbagai stack development.  
Cocok buat pemula yang ingin cepat setup Laravel, NodeJS, atau PHP dengan MySQL tanpa ribet konfigurasi manual.

---

## ✨ Fitur
- Pilihan stack interaktif:
  - Laravel + MySQL
  - NodeJS + MySQL
  - PHP + MySQL
- Auto-generate `docker-compose.yml` dan file konfigurasi
- Bisa memilih lokasi folder project
- Membuat folder project otomatis jika belum ada

---

## 🚀 Cara Install
1. Clone repo:
   ```bash
   git clone https://github.com/Platotel3s/my-py-tools.git
   cd my-py-tools/docker-setup-automator

2. Buat Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate

3. Jalankan Script
```bash
python3 setup.py

