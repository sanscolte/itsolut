# Парсер объявлений

### Как установить

Перейдите в корневую папку и выполните команду:

```shell
pip install -r requirements.txt
```

### Как запустить

Перейдите в папку [parser](parser) и выполните команду:

```shell
python manage.py runserver
```

Перейдите по адресу http://127.0.0.1:8000/

### Как пользоваться

1. auth/register - регистрация
2. auth/login/ - вход в систему
3. api/\<int:pk> - получить детали объявления
4. api/parse/ - спарсить последние 10 объявлений и получить их
