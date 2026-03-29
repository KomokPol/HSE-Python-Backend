docker build -t posts .
docker run -d -p 9000:5432 --name posts posts