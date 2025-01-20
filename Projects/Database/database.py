import pymysql
from .configDB import HOST, USER,PASSWORD,DATABASE


class Database:
    """Класс для подключения к базе данных."""
    
    def __init__(self):
        """Инициализирует все необходимые атрибуты для объекта Database.

        Параметры
        ----------
        host : str
            Адрес хоста базы данных.
        user : str
            Имя пользователя для подключения к базе данных.
        password : str
            Пароль пользователя для подключения к базе данных.
        database : str
            Имя базы данных, к которой осуществляется подключение.
        """
        try:
            self.connection = pymysql.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE
            )
            print("Подключение успешно установлено.")
        except Exception as ex:
            print(f"Ошибка подключения: {ex}")   

    def get_connection(self):
        """Проверяет статус подключения к базе данных.

        Возвращает
        ----------
        bool
            True, если подключение установлено; False, если подключение не установлено.
        """
        if self.connection.open:
            print("Подключение установлено.")
        else:
            print("Подключение не установлено.")
        return self.connection.open

    def close_connection(self):
        """Разрывает активное подключение к базе данных.

        Если есть активное подключение, оно будет закрыто.
        """
        if self.get_connection():
            self.connection.close()
            print("Подключение разорвано.")
        else:
            print("Нет активного соединения для разрыва.")

    def get_query(self, UserID):
        if not self.get_connection():
            self.connection.connect()
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT clients.Name, clients.PhoneNumber, clients.Address, slotstime.TimeSlots AS DATE 
                    FROM appointments 
                    JOIN clients ON appointments.id_Clients = clients.id
                    JOIN slotstime ON appointments.id_SlotsTime = slotstime.id 
                    WHERE clients.UserID = %s
                """, (UserID))
                
                results = cursor.fetchall()
                
                # Возвращаем None или пустой список, если результатов нет
                return results if results else None

        finally:
            self.close_connection()

    def get_available_slots(self):
        if not self.get_connection():
            self.connection.connect()
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM SlotsTime WHERE is_available = 1")
                slots = cursor.fetchall()
                print("Доступные слоты получены.")
                return slots
        except Exception as ex:
            print(f"Ошибка выполнения запроса: {ex}")
            return []

    def get_checkCurrentUser(self, client_id):
        if not self.get_connection():
            self.connection.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"Select clients.UserID from clients where clients.UserID = {client_id}")   
                results = cursor.fetchall() 
                return results if results else None
        except Exception as ex:
            print(f"Ошибка выполнения запроса: {ex}")
        finally:
            self.close_connection()

    def book_slot(self, client_id, slot_id):
        if not self.get_connection():
            self.connection.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE SlotsTime SET is_available = 0 WHERE id = %s", (slot_id,))
                cursor.execute(
                    "INSERT INTO appointments (id_Clients, id_SlotsTime) VALUES (%s, %s)",
                    (client_id, slot_id)
                )
                self.connection.commit()
                print("Слот успешно забронирован.")
                return True
        except Exception as ex:
            print(f"Ошибка выполнения запроса: {ex}")
            return False


    def get_All_register_user(self):
        if not self.get_connection():
            self.connection.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("select clients.UserID, slotstime.TimeSlots, clients.Address from appointments JOIN clients on appointments.id_Clients = clients.id JOIN slotstime on appointments.id_SlotsTime = slotstime.id ")
                results = cursor.fetchall() 
                return results if results else None
        except Exception as ex:
            print(f"Ошибка выполнения запроса: {ex}")
        finally:
            self.close_connection()

    def get_CurrentUser(self, user_id):
        if not self.get_connection():
            self.connection.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT id FROM clients WHERE UserID = {user_id} ORDER BY id DESC LIMIT 1")
                result = cursor.fetchone()  
                return result if result else None 
            
        except Exception as ex:
            print(f"Ошибка выполнения запроса: {ex}")
            return None
        finally:
            self.close_connection()


    def set_query(self, UserID, name, PhoneNumber, Address):
        """Создает запрос на добавление данных в базу данных.

        Если активное подключение отсутствует, оно будет восстановлено.

        Параметры
        ----------
        UserID : int
            Уникальный идентификатор пользователя.
        name : str
            Имя клиента.
        PhoneNumber : str
            Номер телефона клиента.
        Address : str
            Адрес клиента.

        Если запрос выполнен успешно, соединение будет закрыто.
        """
        if not self.get_connection():
            self.connection.connect()
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO clients (UserID, Name, PhoneNumber, Address) VALUES ('{UserID}','{name}','{PhoneNumber}','{Address}')",)
                self.connection.commit()
                print("Успешно добавлен.")
                self.close_connection()  # Закрываем соединение после выполнения запроса
        except Exception as ex:
            print(f"Ошибка выполнения запроса: {ex}")

