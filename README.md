
# Baha Abuse Backend

This is a project that crawled [BaHa(巴哈姆特)](https://www.gamer.com.tw/) forum's articles for administrators.  
To run this backend, the MongoDB is required to store articles.  
Detail [Frontend](http://github.com/jackey8616/BahaAbuse-Frontend) is at there.  

## Requirement
```
python3
MongoDB
```

## Docker
### Build Image
```sh
docker build -t baha-abuse-backend:latest .
```

### Run Image
```sh
docker run -ti -d -p 127.0.0.1:8000:8000 --restart always baha-abuse-backend:latest
```

