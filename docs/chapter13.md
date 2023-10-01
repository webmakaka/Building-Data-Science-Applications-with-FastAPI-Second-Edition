# RUN Project 13

<br/>

```
$ cd ${project_root}
$ source venv/bin/activate
```

<br/>

```
$ uvicorn chapter13.chapter13_api:app
```

<br/>

```
// POST
http --form POST http://localhost:8000/object-detection image@./
assets/coffee-shop.jpg
```

<br/>

**response:**

```

```

<br/>

```
$ uvicorn chapter13.websocket_object_detection.app:app
```

<br/>

http://localhost:8000
