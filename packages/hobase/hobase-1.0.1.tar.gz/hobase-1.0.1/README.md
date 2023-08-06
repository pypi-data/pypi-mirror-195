## HoBase
DataBase основанная на sqlitedict

## Установка
```
pip install hobase
```

## Подключение
```python
from hobase import *
db = Database()
```

## Использование
```python
from hobase import *
# Инициализация датабазы
a = Database(autocommit=True)
# Создание переменной "324234" в "123"
a.set({"324234":"123123"}, UserID(123))
print(a.get(UserID(123))) # Вывод
# Дополнение ещё одной переменной
a.set({"1":"23123"}, UserID(123))
print(a.get(UserID(123)))

# Удаление переменной и проверка
a.delete(id=UserID(123), obj="324234")
print(a.get(id=UserID(123)))

# Закрытие датабазы и проверка output
print(a)
a.close()
print(a)
```