# Yatube API

API for social platform Yatube. Users publish posts, comment, join groups, and follow each other.

## Tech Stack

- Python 3.12, Django 5.1, Django REST Framework 3.15
- JWT auth via SimpleJWT + djoser
- SQLite (development)

## Features

- JWT authentication (create/refresh/verify tokens)
- Posts: create, read, update, delete (author only), pagination
- Comments: nested under posts, CRUD with author-only write
- Groups: read-only list and detail
- Follow system: subscribe to users, search by `?search=`

## Setup

```bash
git clone <repo>
cd yatube_api
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python yatube_api/manage.py migrate
python yatube_api/manage.py runserver
```

## API Endpoints

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/jwt/create/` | Get JWT token pair |
| POST | `/api/v1/jwt/refresh/` | Refresh access token |
| POST | `/api/v1/jwt/verify/` | Verify token validity |

### Posts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/posts/` | List posts (paginated) |
| POST | `/api/v1/posts/` | Create post (auth required) |
| GET | `/api/v1/posts/{id}/` | Post detail |
| PUT/PATCH | `/api/v1/posts/{id}/` | Update post (author only) |
| DELETE | `/api/v1/posts/{id}/` | Delete post (author only) |

### Comments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/posts/{id}/comments/` | List comments |
| POST | `/api/v1/posts/{id}/comments/` | Create comment (auth) |
| GET | `/api/v1/posts/{id}/comments/{cid}/` | Comment detail |
| PUT/PATCH | `/api/v1/posts/{id}/comments/{cid}/` | Update (author only) |
| DELETE | `/api/v1/posts/{id}/comments/{cid}/` | Delete (author only) |

### Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/groups/` | List groups |
| GET | `/api/v1/groups/{id}/` | Group detail |

### Follow

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/follow/` | List follows (auth, filtered by `?search=`) |
| POST | `/api/v1/follow/` | Follow a user (auth) |

## Example Requests

```bash
# Get token
curl -X POST http://localhost:8000/api/v1/jwt/create/ \
  -H 'Content-Type: application/json' \
  -d '{"username": "alice", "password": "secret"}'

# Create post
curl -X POST http://localhost:8000/api/v1/posts/ \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{"text": "Hello world!"}'

# List posts
curl http://localhost:8000/api/v1/posts/

# Add comment
curl -X POST http://localhost:8000/api/v1/posts/1/comments/ \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{"text": "Nice post!"}'

# Follow user
curl -X POST http://localhost:8000/api/v1/follow/ \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{"following": "bob"}'
```

## Tests

```bash
python -m pytest tests/
```

## Author

[Your Name](https://github.com/your-username)
