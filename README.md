# 📬 Mailing Service (Django) — Email Campaign Manager

A Django web application for managing **email campaigns**: recipients, message templates, mailings, manual sending, and delivery attempts history.  
Built as a portfolio/educational project with a focus on **clear CRUD**, **access control**, and **configurable infrastructure** (PostgreSQL / SMTP / optional Redis cache).

---

## ✨ Key Features

- 🔐 **Authentication**
  - Sign up / Sign in / Sign out
  - Password reset flow

- ✅ **Email verification**
  - New users receive a confirmation email
  - Account becomes active after verification

- 👥 **Recipients (Clients)**
  - Create / edit / delete recipients (email, full name, comment)
  - Attach recipients to specific mailings

- 📝 **Message templates (Messages)**
  - Create templates (subject + body)
  - Reuse templates across multiple mailings

- 📅 **Mailings**
  - Configure **start/end** time window
  - Assign a template and a list of recipients
  - Change mailing status

- 🚀 **Sending**
  - Manual sending from UI
  - Sending via management command (for mailings active by time window)

- 🧾 **Attempts & logs**
  - Each send attempt is recorded (success/failure)
  - Stored: timestamp, status, server response / error text

- 🛡️ **Permissions**
  - Regular users manage **only their own objects** (`owner`)
  - Superuser/admin has access to everything

- 📊 **Homepage statistics**
  - Total mailings, active mailings, unique clients
  - 🧠 Optional caching via Redis (`CACHE_ENABLED`)

---

## 🧰 Tech Stack

- **Python** 3.x  
- **Django** 5.x  
- **PostgreSQL**  
- **SMTP** (email sending)  
- **Redis** (optional caching)  
- **Poetry** (dependency management)

---

## 🚀 Quick Start (Local)

### 1) Clone & install dependencies

#### Option A — Poetry (recommended)
```bash
poetry install --no-root
poetry run python -V
```

> If Poetry tries to install the project as a package and fails, use `--no-root` (recommended for Django repos).

#### Option B — venv + pip
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

---

### 2) Create `.env`

Copy the example:
```bash
cp .env.example .env
```

Fill in values (example):
```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# PostgreSQL
DB_NAME=mailing_db
DB_USER=mailing_user
DB_PASSWORD=mailing_pass
DB_HOST=localhost
DB_PORT=5432

# Email (SMTP example — replace with your provider)
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_SSL=True
DEFAULT_FROM_EMAIL=your-email@example.com

# Cache
CACHE_ENABLED=False
```

---

### 3) Create PostgreSQL database

Open psql:
```bash
psql postgres
```

Create user/db:
```sql
CREATE USER mailing_user WITH PASSWORD 'mailing_pass';
CREATE DATABASE mailing_db OWNER mailing_user;
GRANT ALL PRIVILEGES ON DATABASE mailing_db TO mailing_user;
\q
```

---

### 4) Run migrations & create admin

```bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```

---

### 5) Run the server

```bash
poetry run python manage.py runserver
```

Open:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin/

---

## 🧪 Development Mode: print emails to console

If you don’t want to configure SMTP locally, you can output emails directly to the terminal:

Add to `.env`:
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

And make sure `settings.py` uses it (typical pattern):
```python
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)
```

✅ Then password reset / verification links will appear in the server console.

---

## ✉️ SMTP Notes (Real Email Sending)

- Use **app passwords** for your email provider (recommended/required by many services).
- If you see SSL errors like:
  - `ssl.SSLCertVerificationError: CERTIFICATE_VERIFY_FAILED`

This usually means **local certificates** on your machine are missing or not trusted (environment issue).  
On macOS with python.org installations, you may need to run *Install Certificates.command*.

---

## 🧠 Redis Cache (Optional)

To enable caching:
1) Start Redis (example for macOS/Homebrew):
```bash
brew install redis
brew services start redis
```

2) Set in `.env`:
```env
CACHE_ENABLED=True
```

---

## 🛠 Management Commands

- Create “Managers” group and assign permissions:
```bash
poetry run python manage.py create_groups
```

- Send active mailings (within configured start/end window):
```bash
poetry run python manage.py send_mailings
```

---

## 🔒 Security Notes

- Do **not** commit real credentials into the repository.
- Keep `.env` in `.gitignore` (use `.env.example` for placeholders).
- Avoid committing runtime/cache artifacts like `dump.rdb` from Redis.

---

## 🧩 Roadmap (Nice-to-have)

- ⏱ Scheduled sending (Celery / APScheduler / cron)
- 📨 HTML emails, attachments, unsubscribe flow
- ✅ Automated tests + coverage report
- 🎨 UI improvements (Bootstrap navbar, tables, badges)

---

---

# 📬 Сервис рассылок (Django) — менеджер email-кампаний

Веб-приложение на Django для управления **email-рассылками**: получатели, шаблоны писем, рассылки, ручная отправка и история попыток.  
Проект сделан как учебный/портфолио, с упором на **CRUD**, **права доступа** и настраиваемую инфраструктуру (PostgreSQL / SMTP / Redis-кеш по желанию).

---

## ✨ Возможности

- 🔐 **Аутентификация**
  - регистрация / вход / выход
  - восстановление пароля

- ✅ **Подтверждение email**
  - после регистрации отправляется письмо со ссылкой
  - аккаунт активируется после подтверждения

- 👥 **Получатели (Clients)**
  - добавление / редактирование / удаление клиентов (email, ФИО, комментарий)
  - привязка клиентов к рассылкам

- 📝 **Шаблоны писем (Messages)**
  - создание шаблонов (тема + текст)
  - повторное использование шаблонов в разных рассылках

- 📅 **Рассылки (Mailings)**
  - окно активности **start/end**
  - выбор шаблона и списка получателей
  - статусы рассылки

- 🚀 **Отправка**
  - ручной запуск из интерфейса
  - отправка через management command (для активных по времени рассылок)

- 🧾 **Логи/история**
  - каждая попытка отправки сохраняется (успех/ошибка)
  - хранится дата/время, статус, текст ошибки/ответ сервера

- 🛡️ **Права доступа**
  - обычный пользователь управляет только своими объектами (`owner`)
  - админ/superuser видит всё

- 📊 **Статистика на главной**
  - всего рассылок, активных рассылок, уникальных клиентов
  - 🧠 опционально кешируется через Redis (`CACHE_ENABLED`)

---

## 🧰 Стек

- **Python** 3.x  
- **Django** 5.x  
- **PostgreSQL**  
- **SMTP** (отправка писем)  
- **Redis** (кеш — опционально)  
- **Poetry** (зависимости)

---

## 🚀 Быстрый старт (локально)

### 1) Установка зависимостей

#### Вариант A — Poetry (рекомендую)
```bash
poetry install --no-root
poetry run python -V
```

> Если Poetry пытается установить проект как пакет и ругается — используйте `--no-root` (для Django это нормально).

#### Вариант B — venv + pip
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

---

### 2) Создай `.env`

Скопируй пример:
```bash
cp .env.example .env
```

Заполни значения (пример):
```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# PostgreSQL
DB_NAME=mailing_db
DB_USER=mailing_user
DB_PASSWORD=mailing_pass
DB_HOST=localhost
DB_PORT=5432

# Email (SMTP пример — замени на свой провайдер)
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_SSL=True
DEFAULT_FROM_EMAIL=your-email@example.com

# Cache
CACHE_ENABLED=False
```

---

### 3) Создай базу PostgreSQL

```bash
psql postgres
```

```sql
CREATE USER mailing_user WITH PASSWORD 'mailing_pass';
CREATE DATABASE mailing_db OWNER mailing_user;
GRANT ALL PRIVILEGES ON DATABASE mailing_db TO mailing_user;
\q
```

---

### 4) Миграции и суперпользователь

```bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```

---

### 5) Запуск

```bash
poetry run python manage.py runserver
```

Открыть:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin/

---

## 🧪 Режим разработки: письма в консоль

Чтобы не настраивать SMTP локально, можно выводить письма в терминал.

Добавь в `.env`:
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

И убедись, что `settings.py` это читает:
```python
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)
```

✅ Тогда ссылки подтверждения/сброса пароля будут печататься в консоль сервера.

---

## ✉️ SMTP (реальная отправка)

- Используй **пароли приложений** (app passwords).
- Если видишь ошибку SSL типа:
  - `ssl.SSLCertVerificationError: CERTIFICATE_VERIFY_FAILED`

Это обычно проблема **локальных сертификатов** на конкретной машине (не проблема репозитория).  
На macOS с python.org Python часто помогает запуск *Install Certificates.command*.

---

## 🧠 Redis (опционально)

1) Запусти Redis (пример для macOS/Homebrew):
```bash
brew install redis
brew services start redis
```

2) В `.env`:
```env
CACHE_ENABLED=True
```

---

## 🛠 Команды

- Создать группу “Менеджеры” и назначить права:
```bash
poetry run python manage.py create_groups
```

- Отправить активные рассылки (по start/end):
```bash
poetry run python manage.py send_mailings
```

---

## 🔒 Безопасность

- Не коммить реальные пароли/логины/ключи в репозиторий.
- `.env` должен быть в `.gitignore`, а `.env.example` — только с плейсхолдерами.
- Не коммить артефакты типа `dump.rdb` (дамп Redis).

---

## 🧩 Идеи улучшений

- ⏱ Планировщик (Celery / APScheduler / cron)
- 📨 HTML-письма, вложения, отписка (unsubscribe)
- ✅ Тесты + отчёт покрытия
- 🎨 Улучшение UI (navbar, таблицы, бейджи статусов)
