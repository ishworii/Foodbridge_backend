# FoodBridge Backend

> **Local Food Rescue & Redistribution Network**

This repository contains the backend API for FoodBridge, built with Django and Django REST Framework (DRF). It provides functionality for user registration, authentication, donation management, claiming, and a robust admin dashboard.

---

## 🗂 Table of Contents

1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)
3. [Models](#models)
4. [API Endpoints](#api-endpoints)
5. [Authentication](#authentication)
6. [User Roles](#user-roles)
7. [Admin Features](#admin-features)
8. [Testing](#testing)

---

## Project Overview

FoodBridge connects individuals willing to donate surplus food (Donors) with people in need (Receivers). The backend API allows:

* **User registration** with role selection
* **JWT-based authentication**
* **CRUD operations for donations**
* **Claiming donations**
* **Role-based permissions**
* **Admin dashboard endpoints for statistics and management**

---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd foodbridge-backend
   ```
2. **Create virtual environment & install dependencies**
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
3. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```
5. **Run development server**
   ```bash
   python manage.py runserver
   ```

---

## Models

### Profile
* `user` — OneToOne to `User`
* `role` — Choice of `donor` or `receiver`

### Donation
* `donor` — ForeignKey to `User`
* `title`, `description`, `quantity`, `location`, `food_type`, `expiry_date`, `image`
* `is_claimed` — BooleanField
* `claimed_by` — ForeignKey to `User` (nullable)
* `created_at` — DateTimeField

---

## API Endpoints

### Registration & Authentication
* `POST /api/register/` — Register a new user
* `POST /api/token/` — Obtain JWT tokens
* `POST /api/token/refresh/` — Refresh access token

### Donation Management
* `GET    /api/donations/` — List all donations
* `POST   /api/donations/` — Create a donation (Donor only)
* `GET    /api/donations/{id}/` — Retrieve a donation
* `PUT    /api/donations/{id}/` — Update a donation (Donor only)
* `DELETE /api/donations/{id}/` — Delete a donation (Donor only or Admin)
* `POST   /api/donations/{id}/claim/` — Claim a donation (Receiver only)
* `GET    /api/donations/claimed_by_user/?user_id={id}` — Claimed donations for current user

### User Management
* `GET /api/users/{id}/donations/` — Donations by a specific user
* `GET /api/me/` — Current user profile

### Admin Endpoints
* `GET /api/admin/stats/` — Platform statistics
* `GET /api/admin/donations/` — Manage all donations
* `DELETE /api/admin/donations/{id}/` — Delete any donation (Admin only)

---

## Authentication

* Uses **Simple JWT**
* Add header:
  ```
  Authorization: Bearer <access_token>
  ```

---

## User Roles

* **Donor**: Can create, edit, and delete their own donations
* **Receiver**: Can claim available donations
* **Admin**: Can manage all donations and view platform statistics

---

## Admin Features

- **Admin Dashboard Endpoints**: For statistics, trends, and donation management
- **Full CRUD for Donations**: Admins can edit/delete any donation
- **User Statistics**: Track user roles and activity

---

## Testing

1. Register users with roles
2. Login to obtain JWT tokens
3. Create donations as Donor
4. Attempt unauthorized actions (e.g., Receiver creating donation)
5. Claim donation as Receiver
6. Verify double-claim protection
7. List and filter donations

---

## License

This project is part of the FoodBridge platform.

