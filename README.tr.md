<p align="center">
    <img src="app/log_screen/static/favicon_io/android-chrome-512x512.png" height="128">
    <h1 align="center">Personel Kayıt Ekranı</h1>
</p>

[![Python - 3.11](https://img.shields.io/badge/Python-3.11-2ea44f)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/nazimcanislam/employee-log-screen/blob/main/LICENSE)

Personel ve müşteri ekleyip, projeleri ilişkilendirmeye yarayan Django kullanan arayüz.

## Gereksinimler

- Python 3.11
- Django 4.1
- Pyscopg2
- PostgreSql 15
- Docker

## Sunucuyu Çalıştırmak

### Veri Tabanını Tanımla

Django sunucusunun PostgreSql ile iletişime geçebilmesi için gerekli olan bilgileri `app/.env` dosyasındaki alanların karşılarına yazmak gerekir. Eğer bu dosya yok ise oluşturun.

```
DEBUG=<True ya da False>
SECRET_KEY=verysecret
ALLOWED_HOSTS=*

POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

SQL_HOST=db
SQL_PORT=5432
```

### Docker İmajı Oluştur ve Çalıştır

Geliştirme ve ürün imajları oluşturabiliriz.

#### Geliştirme İçin

Bu komut `docker-compose.dev.yml` dosyasındaki veriler ile imajlar oluşturup çalıştırır.

```bash
docker-compose -f docker-compose.dev.yml up
```

#### Ürün Haline Getirmek İçin

`app/.env` dosyası hazır olduğunda ürünselleştirmek için olan imajı oluşturun ve çalıştırmak için bu komudu girin. Ayrıca `-d` eki sayesinde uygulama arka planda çalışır.

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Artık uygulamanız <a href="http://127.0.0.1:8000">127.0.0.1:8000</a>. adresinde çalışır halde.

<h3>Süper Kullanıcı Oluştur</h3>

Uygulamayı durdurduktan sonra konteynırın içinden Django'ya bir süper kullanıcı oluşturmasını söylemek için:

```bash
docker-compose -f docker-compose.prod.yml run web python manage.py createsuperuser
````


- `-f` kısaca geliştirme ortamını oluşturmak ve tabii ki ürünselleştirme imajlarını oluşturup çalıştırmak için gerekli ayar dosyalarını belirtir. Geliştirme için `docker-compose.dev.yml`, ürünselleştirme için `docker-compose.prod.yml` dosyasını kullanın.
- `web`, Django uygulamasının Docker konteynır adıdır.
- Bu komutu girdikten sonra süper kullanıcı oluşturmak için kullanıcı adı ve parola girmeniz gerekir.

Şimdi tekrar docker imajını çalıştıraiblirsiniz!
