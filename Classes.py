# Начальные запасы товаров 
initial_store_items = {"печеньки": 10, "собачки": 10, "коробки": 10, "конфеты": 10, 
"игрушки": 10} 

initial_shop_items = {"собачки": 2, "коробки": 5}

from abc import ABC, abstractmethod # дочерние классы обязаны реализовать создаваемые методы
class Storage(ABC): # Наследование от стандартного абстрактного класса 
 """ 
Абстрактный класс для описания хранилища товаров. 
""" 
 def __init__(self, items: dict, capacity: int): 
  self._items = items.copy()        
# словарь {товар: количество} ввиде словаря
  self._capacity = capacity # общая вместимость ввиде числа
 
 @abstractmethod 
 def add(self, name: str, amount: int)  -> None: # Любое конкретное хранилище имеет этот метод
  """ 
Увеличивает количество товара name на amount. 
""" 
  pass
 

 @abstractmethod
 def remove(self, name: str, amount: int) -> None: 
  """ 
Уменьшает количество товара name на amount. 
""" 
  pass


 def get_free_space(self) -> int: 
  """ 
Возвращает количество свободного места в хранилище. 
""" 
  return self._capacity - sum(self._items.values()) 


 def get_items(self) -> dict: 
  """ 
Возвращает текущее содержимое хранилища. 
""" 
  return self._items.copy() # возвращаем копию, чтобы нельзя было менять снаружи  


 def get_unique_items_count(self) -> int: 
  """ 
Возвращает количество уникальных позиций товара. 
""" 
  return len(self._items)

 
 
 
 
class Store(Storage): 
 """ 
Склад. Не имеет ограничений на количество видов товаров. 
""" 


 def __init__(self, items: dict, capacity: int = 100): 
# корректный вызов конструктора родителя 
  super().__init__(items,capacity)  


 def add(self, name: str, amount: int) -> None: 
  """ 
Добавляет товары на склад. 
Если количество превышает свободное место - выводит сообщение об 
ошибке. 
""" 
# реализация логики добавления 
  if not isinstance(amount, int) or isinstance(amount,bool) or amount <= 0:
   raise ValueError("Ошибка ввода!")
 
  if  self.get_free_space() < amount: 
   raise ValueError("Ошибка ввода!")

  self._items[name] = self._items.get(name, 0) +  amount


 def remove(self, name: str, amount: int) -> None: 
  """
Забирает товары со склада. 
Если запрашиваемого количества нет - выводит сообщение об ошибке. 
""" 
# реализация логики удаления 
  if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
   raise ValueError("Ошибка ввода!")
 
  if  self._items.get(name, 0) < amount:
    raise ValueError("Недостаточно товара на складе!")

  self._items[name] = self._items[name] - amount 
 
  if self._items[name] == 0:
   del self._items[name]
 
  
  
  
    
class Shop(Storage): 
 """ 
Магазин. Ограничение: не более 5 уникальных товаров. 
""" 
 def __init__(self, items: dict, capacity: int = 20): 
# корректный вызов конструктора родителя 
  super().__init__(items,capacity)  


 def add(self, name: str, amount: int) -> None: 
  """ 
Добавляет товары в магазин. 
Проверяет два условия: 
1. Хватит ли места по вместимости? 
2. Не превысит ли добавление лимит в 5 уникальных товаров? 
Если любое из условий нарушено - выводит сообщение об ошибке. 
""" 
# реализация логики добавления с проверкой ограничений 
  if not isinstance(amount, int) or isinstance(amount,bool) or amount <= 0:
   raise ValueError("Ошибка ввода!")
 
  if  self.get_free_space() < amount: 
   raise ValueError("Не хватает места!")

  if  name not in self._items and self.get_unique_items_count() >= 5:
   raise ValueError("Превышен лимит добавления уникальных товаров!")

  self._items[name] = self._items.get(name, 0) +  amount
 
 
 def remove(self, name: str, amount: int) -> None: 
  """ 
Забирает товары из магазина. 
Если запрашиваемого количества нет - выводит сообщение об ошибке. 
""" 
# реализация логики удаления 
  if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
    raise ValueError("Ошибка ввода!")
  
  if  self._items.get(name, 0) < amount:
     raise ValueError("Недостаточно товара в магазине!")
 
  self._items[name] = self._items[name] - amount 
  
  if self._items[name] == 0:
    del self._items[name]
  
 
class Request: 
 """ 
Класс для представления запроса на перемещение товаров. 
""" 
 def __init__(self, request_str: str): 
  parts = request_str.split()
  
  if  len(parts) != 7:
     raise ValueError("Неверный формат запроса!")
  
  
  try:
      self.amount = int(parts[1])
  except ValueError:
      raise ValueError("Колличество должно быть числом!")
    
  self.product = parts[2]
  self.from_point = parts[4]
  self.to_point = parts[6]
  """ 
Парсит строку запроса. 
Пример входящей строки: "Доставить 3 печеньки из склад в магазин" 
""" 
# Задача: 
# 1. Разбить строку request_str на части (по пробелам). 
# 2. Проверить, что количество частей достаточно. 
# 3. Извлечь и преобразовать в числа количество (amount). 
# 4. Извлечь название товара (product). 
# 5. Извлечь точки отправления (from_point) и назначения (to_point). 
# 6. Сохранить все в атрибуты экземпляра. 
  """
 self.amount = 0 
 self.product = "" 
 self.from_point = "" 
 self.to_point = ""
 """ 
# Можно ожидать строго определенный порядок слов: 
#    [0]     [1]   [2]     [3]  [4]  [5]  [6] 
# "Доставить  3  печеньки  из  склад  в  магазин" 


 def __repr__(self) -> str: 
  """Возвращает понятное строковое представление запроса.""" 
  return f"Доставить {self.amount} {self.product} из {self.from_point} в{self.to_point}"

  