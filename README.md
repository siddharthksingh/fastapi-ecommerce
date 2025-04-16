# 🛒 FastAPI-ecommerce

This is a lightweight eCommerce backend built with **FastAPI** and **MongoDB**. It supports user authentication with JWT tokens, role-based access control, product management, cart functionality, and order placement.

## 🚀 Features

- FastAPI backend with JWT-based authentication
- MongoDB as the database (using Motor - async driver)
- Role-based access for protected routes
- Add to cart, view cart, place orders
- Admin-only routes for product/user management
- Dockerized setup with Docker Compose

---

## 🧱 Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Containerization**: Docker + Docker Compose

---

## 📦 Setup

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Clone this repository
- Run the command:
```bash
docker-compose up --build -d
```