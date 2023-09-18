# RUN Project 12

<br/>

```
$ cd ${project_root}
$ source venv/bin/activate
```

<br/>

```
$ uvicorn chapter12.chapter12_prediction_endpoint:app
```

<br/>

```
// POST
$ curl \
    --data '{
      "text":"computer cpu memory ram"
      }' \
    --header "Content-Type: application/json" \
    --request POST \
    --url http://localhost:8000/prediction \
    | jq
```

<br/>

**response:**

```
{
  "category": "comp.sys.mac.hardware"
}
```

<br/>

```
$ uvicorn chapter12.chapter12_async_not_async:app
```

<br/>

```
$ curl http://localhost:8000/slow-async
$ curl http://localhost:8000/fast


$ curl http://localhost:8000/slow-sync
$ curl http://localhost:8000/fast
```
