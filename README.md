# API для проекта YaTube
## Как запустить проект:

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Tiaki026/api_final_yatube.git
```

```
cd api_yatube
```

### Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Выполнить миграции:

```
python manage.py migrate
```

### Запустить проект:

```
python manage.py runserver
```