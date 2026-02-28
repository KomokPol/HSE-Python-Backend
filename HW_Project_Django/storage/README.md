# Storage

## Конфигурация

- **База данных:** posts
- **Пользователь:** KomokPol
- **Пароль:** KomokPol
- **Порт:** 9000

## Запуск базы данных

```bash
cd storage
chmod +x run.sh stop.sh
./run.sh
```

## Остановка базы данных

```bash
cd storage
./stop.sh
```

## Применение миграций

После того, как запустили бд, вернитесь в корень проекта и выполните:

```bash
cd ..
make migrations
```

Или вручную:

```bash
python manage.py migrate
```

Что должно создасться:
1. `0001_initial`: создание таблиц User, Post, Comment
2. `0002_mock_data`: заполнение бд тестовыми данными (5 пользователей, 6 постов, 8 комментариев с лайками)

## Откат мок-данных

Чтобы удалить тестовые данные, сохранив структуру таблиц:

```bash
python manage.py migrate backend 0001_initial
```

## Создание новых миграций

При изменении моделей:

```bash
make create_migrations
make migrations
```

## Загрузка фикстуры вручную

```bash
python manage.py loaddata mock_data
```
