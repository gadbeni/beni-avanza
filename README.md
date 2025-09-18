"# beni-avanza" 

docker run -e DATABASE_NAME=beni_avanza -e DATABASE_USER=root -e DATABASE_PASSWORD="" -e DATABASE_HOST=host.docker.internal -e DATABASE_PORT=3306 -e DJANGO_SECRET_KEY="your-secret-key" -e DEBUG=True -e ALLOWED_HOSTS="localhost,127.0.0.1,host.docker.internal" -p 8000:8000 -t beni-avanza