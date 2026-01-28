# API Endpoint Testing

Manual curl commands to test each endpoint against the Supabase-connected Flask API.

**Prerequisites:** Start the server with `python3 run.py` (runs on `http://localhost:5001`)

---

## Health Check

```bash
curl -s http://localhost:5001/api/ | python3 -m json.tool
```

---

## Hello World

```bash
curl -s http://localhost:5001/api/helloworld/ | python3 -m json.tool
```

---

## Todos CRUD Operations

### List All Todos

```bash
curl -s http://localhost:5001/api/todos/ | python3 -m json.tool
```

### Get Single Todo

Replace `3` with an existing todo ID:

```bash
curl -s http://localhost:5001/api/todos/3 | python3 -m json.tool
```

### Create New Todo

```bash
curl -s -X POST http://localhost:5001/api/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My new todo"}' | python3 -m json.tool
```

### Update Todo

Replace `3` with the todo ID to update:

```bash
curl -s -X PUT http://localhost:5001/api/todos/3 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated title"}' | python3 -m json.tool
```

### Delete Todo

Replace `3` with the todo ID to delete:

```bash
curl -s -X DELETE http://localhost:5001/api/todos/3 -w "Status: %{http_code}\n"
```

---

## Error Cases

### Get Non-Existent Todo (404)

```bash
curl -s http://localhost:5001/api/todos/99999 | python3 -m json.tool
```

### Create Todo Without Title (400)

```bash
curl -s -X POST http://localhost:5001/api/todos/ \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool
```

### Update Non-Existent Todo (404)

```bash
curl -s -X PUT http://localhost:5001/api/todos/99999 \
  -H "Content-Type: application/json" \
  -d '{"title": "Will fail"}' | python3 -m json.tool
```

### Delete Non-Existent Todo (404)

```bash
curl -s -X DELETE http://localhost:5001/api/todos/99999 | python3 -m json.tool
```

---

## Swagger Documentation

Open in browser: http://localhost:5001/api/docs
