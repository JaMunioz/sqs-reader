# Usa una imagen de Python como base
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo readSQS.py al contenedor
COPY readSQS.py /app/

# Instala las dependencias necesarias
RUN pip install boto3 python-dotenv

# Ejecuta el script cuando se inicie el contenedor
CMD ["python", "readSQS.py"]
