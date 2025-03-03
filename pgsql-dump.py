import os
import boto3
from datetime import datetime

def main():
    # Выполняет команду pg_dump для создания резервной копии PostgreSQL в текстовом формате
    os.system('pg_dump -h $PG_HOST -U $PG_USER --encoding UTF8 --no-owner --no-privileges --format plain $PG_DATABASE > pgsql.sql')

    # Проверяет, создан ли файл резервной копии
    if os.path.exists('pgsql.sql'):
        source_path = 'pgsql.sql'
        # Формирует уникальное имя файла резервной копии на основе текущей даты и времени
        destination_filename = source_path + '_' + datetime.strftime(datetime.now(), "%Y.%m.%d.%H:%M") + 'UTC' + '.backup'
        # Вызывает функцию для загрузки файла в S3
        upload_to_s3(source_path, destination_filename)

def upload_to_s3(source_path, destination_filename):
    # Создает клиент S3 с использованием учетных данных из переменных окружения
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        endpoint_url=os.getenv('AWS_HOST'),
    )
    s3.list_buckets()    
    print(s3.list_buckets())
    # Получает имя бакета из переменной окружения
    bucket_name = os.getenv('AWS_BUCKET_NAME')

    # Файл резервной копии загружает в указанный бакет
    with open(source_path, "rb") as data:
        s3.upload_fileobj(data, bucket_name, destination_filename)

if __name__ == '__main__':
    # Вызывает функцию main, если скрипт выполняется как самостоятельное приложение
    main()