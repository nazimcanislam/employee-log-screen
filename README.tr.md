# <img src="log_screen/static/favicon_io/favicon-32x32.png"> Personel Kayıt Ekranı

Personel ve müşteri ekleyip, projeleri ilişkilendirmeye yarayan Django kullanan arayüz.

## Gereksinimler

- Python 3.11
- Django 4.1
- Pyscopg2
- PostgreSql 15

## Sunucuyu Çalıştırmak

### Veri Tabanını Tanımla

Django sunucusunun PostgreSql ile iletişime geçebilmesi için gerekli olan bilgileri `.env` dosyasındaki alanların karşılarına yazmak gerekir.

```
DB_NAME=example_db_name
DB_USER=example_user_name
DB_PASSWORD=verysecretpassword
DB_HOST=127.0.0.1
DB_PORT=5432
```

### Python İçin Sanal Ortam Oluştur

Django ve diğer gerekli kütüphaneler için sanal ortam oluşturalım...

```bash
python3 -m virtualenv venv
```

Sanal ortamı çalıştıralım (Windows)

```powershell
.\venv\Scripts\activate.bat
```

Sanal ortamı çalıştıralım (Unix)

```bash
./venv/bin/activate
```

Gerekli kütüphaneleri kuralım...

```bash
pip install -r requirements.txt
```

### Veri Tabanı Tablolarını Onaylamak

Django projemizin modellerini onaylamak için yazacağımız kodlar...

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### Süper Kullanıcı Oluşturmak

Uygulamayı kullanabilmek için bir süper kullanıcıya ihtiyamıcız var. Django'nun komut satırı ile süper kullanıcımızı oluşturabiliriz.

```bash
python manage.py createsuperuser
```

### Sunucuyu Başlatmak

Proje klasöründe çalıştıracağımız kod...

```bash
python manage.py runserver
```

Artık proje <a href="http://127.0.0.1:8000">127.0.0.1:8000</a> adresinde sunucumuz çalışır halde.
