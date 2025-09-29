# Imagen base de Python ligera
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar los requisitos e instalarlos
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto de Flask
EXPOSE 5000

# Comando para ejecutar la app
CMD ["python", "app.py"]
