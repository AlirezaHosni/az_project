# Moshaver

#### **1. https://github.com/OstadMoshaver/Back.git** (terminal)

#### **2. pip install -r requirements.txt** (terminal, with active virtualenv)

#### **3. create database with this info:**  (mysql)


        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.mysql"),
        "NAME": os.environ.get("SQL_DATABASE", "moshaver_db"),
        "USER": os.environ.get("SQL_USER", "root"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", ""),
        "HOST": os.environ.get("SQL_HOST", "localhost"),

    - Set the **Charset to utf8mb4**, and **Collaction to utf8mb4_general** when creating database in mysql.

#### **4. python manage.py makemigrations** (terminal)

#### **5. python manage.py migrate** (terminal)

#### **6. python manage.py runserver** (terminal)
