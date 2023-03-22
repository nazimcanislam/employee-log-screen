# <img src="app/log_screen/static/favicon_io/favicon-32x32.png"> Personel Kayıt Ekranı

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
DB_NAME=example_db_name
DB_USER=example_user_name
DB_PASSWORD=verysecretpassword
DB_HOST=127.0.0.1
DB_PORT=5432
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
