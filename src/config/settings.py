from dotenv import load_dotenv
import os

# Загрузка переменных из файла .env
load_dotenv()

# Получение значения переменной MONGODB_HOST
MONGODB_HOST = os.getenv('MONGODB_HOST')
BATCH_SIZE = os.getenv('BATCH_SIZE')
