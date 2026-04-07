# 🚀 Instadew Backend

## 📌 Overview

**Instadew** is a real-time messaging backend system designed to power a modern chat application similar to platforms like Telegram or WhatsApp.
This backend is built with scalability, security, and real-time communication in mind.

The project is currently under active development, with new features being continuously added and improved.

---

## 🎯 Core Features

### 🔐 Authentication & Authorization

* User registration and login
* JWT-based authentication (Access + Refresh tokens)
* Automatic token refreshing
* Secure password hashing
* Protected routes for authenticated users only

---

### 💬 Real-Time Messaging

* WebSocket-based communication
* Instant message delivery
* One-to-one private chats
* Real-time typing indicators (planned)
* Message status (sent, delivered, seen)

---

### 👥 User Management

* User profile creation
* Profile update (username, avatar, bio)
* User search functionality
* Online/offline status tracking

---

### 📂 Chat System

* Create private conversations
* Retrieve chat history
* Pagination for messages
* Message timestamps
* Read/unread message tracking

---

### 📡 WebSocket System

* Persistent connections
* Real-time event handling
* Scalable architecture for multiple users
* Channel-based communication

---

### 🗄️ Database

* PostgreSQL database
* Optimized queries for performance
* Relational structure for users, chats, and messages

---

### ⚙️ API System

* RESTful API endpoints
* Clean and modular architecture
* JSON-based communication
* Error handling and validation

---

### 🔒 Security

* JWT authentication
* Input validation
* Protection against common vulnerabilities
* Secure token storage strategy

---

### 📊 Logging & Monitoring (Planned)

* Request logging
* Error tracking
* Performance monitoring

---

### ☁️ Deployment Ready

* Docker support
* Docker Compose setup
* Environment-based configuration
* Production-ready structure

---

## 🏗️ Project Structure

```
instadew-backend/
│
├── app/
│   ├── models/        # Database models
│   ├── schemas/       # Validation schemas
│   ├── routes/        # API endpoints
│   ├── services/      # Business logic
│   ├── websocket/     # WebSocket handlers
│   └── core/          # Settings & config
│
├── migrations/        # Database migrations
├── docker/            # Docker configs
├── .env               # Environment variables
├── docker-compose.yml
└── main.py            # Entry point
```

---

## ⚡ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sobir0630/instadew-backend.git
cd instadew-backend
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost:5432/instadew
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## 🐳 Run with Docker

```bash
docker-compose up --build
```

---

## ▶️ Run Locally

```bash
uvicorn main:app --reload
```

---

## 🔗 API Endpoints (Examples)

### Auth

* `POST /auth/register`
* `POST /auth/login`
* `POST /auth/refresh`

### Users

* `GET /users/me`
* `PUT /users/update`
* `GET /users/search`

### Chats

* `GET /chats/`
* `POST /chats/create`

### Messages

* `GET /messages/{chat_id}`
* `POST /messages/send`

---

## 🔌 WebSocket Endpoint

```
ws://localhost:8000/ws/chat/{chat_id}
```

---

## 🚧 Future Improvements

* Group chats
* Voice & video calls
* File/image sharing
* Push notifications
* AI-based chat features
* End-to-end encryption
* Message reactions

---

## 💡 Use Case

Instadew backend is designed to:

* Handle real-time communication systems
* Serve as a foundation for chat apps
* Demonstrate scalable backend architecture

---

## 🧠 Technologies Used

* Python
* FastAPI / Django (depending on your implementation)
* PostgreSQL
* WebSockets
* Docker

---

## 👨‍💻 Author

**Sobirjon Mamasoliyev**

Backend Developer | Real-time Systems Enthusiast

---

## 📌 Status

🚀 **Actively in development**
New features and improvements are continuously being added.

---

## ⭐ Notes

This project is part of a larger vision to build a scalable, production-ready messaging platform capable of handling real-time communication at scale.

---
