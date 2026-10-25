from Classes import Store
from Classes import Shop
from Classes import Request

initial_store_items = {"печеньки": 10, "собачки": 10, "коробки": 10,
"конфеты": 10, "игрушки": 10} 
initial_shop_items = {"собачки": 2, "коробки": 5}

def main(): 
 """ 
Точка входа в программу. 
""" 
# 1. Инициализировать хранилища 
 store = Store(items = initial_store_items)
 shop = Shop(items = initial_shop_items) 


# 2. Главный цикл программы 
 while True: 
# 2.1. Вывести текущее состояние хранилищ 
     print("\nТекущие запасы:") 
     print(f"Склад: {store.get_items()}") 
     print(f"Магазин: {shop.get_items()}") 
 
# 2.2. Получить запрос от пользователя 
     user_input = input("\nВведите запрос структуры"
                        "\n’Доставить *кол-во* *товар* из *откуда* в *куда*’"
                        "\n(или 'стоп' / 'выход' для выхода)\n->").strip() 
 
     if user_input.lower() in ('стоп', 'выход'): 
      print("Спасибо за использование системы доставки!") 
      break 

# 2.3. Создать объект запроса и распарсить ввод 
     try: 
         request = Request(user_input) 
     except ValueError:
            print("Неправильный формат запроса. Попробуйте снова.") 
            continue 


# 2.4. Определить, откуда и куда везем 
# сопоставить request.from_point и request.to_point с объектами store и shop.
# Например, через словарь. 

   
     storages = {"склад": store, "магазин": shop} 

     from_storage = storages.get(request.from_point) 

     to_storage = storages.get(request.to_point)
 
     if from_storage is None or to_storage is None: 
       print("Указано неверное название хранилища."
             "Используйте 'склад' или 'магазин'.") 
       continue 
     if from_storage is to_storage:
         print("Исходное и целевое хранилище должны различаться")
         continue
     
# 2.5. Проверить возможность перемещения 
# Проверить наличие товара в from_storage

     
     if (request.product not in from_storage.get_items()
         or from_storage.get_items()[request.product] < request.amount): 
      print(f"Нельзя выполнить запрос: недостаточно товара"
            f"'{request.product}' в '{request.from_point}'.") 
      continue 

# Проверить возможность добавления в to_storage 
     if to_storage.get_free_space() < request.amount: 
      print(f"Нельзя выполнить запрос: недостаточно места в '{request.to_point}'.") 
      continue 
  
# необходимо учесть ограничения Shop (макс. 5 товаров) при добавлении нового тов. 
     if (isinstance(to_storage, Shop)
         and request.product not in to_storage.get_items()
         and to_storage.get_unique_items_count() >= 5 ):
         print ("Нельзя выполнить запрос магазин уже содержит 5 видов товаров.")
         continue
# 2.6. Выполнить перемещение и составить отчет 
     print(f"Курьер забирает {request.amount} {request.product}"  
           f"из {request.from_point}...") 

     from_storage.remove(request.product, request.amount) 

     print(f"Курьер везет {request.amount} {request.product}"
           f"из {request.from_point} в {request.to_point}...") 

     to_storage.add(request.product, request.amount) 

     print(f"Курьер доставил {request.amount} {request.product}"
           f"в {request.to_point}.") 
 
if __name__ == "__main__": 
  
   main()