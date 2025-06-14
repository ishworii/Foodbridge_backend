# FoodBridge Backend

> **Local Food Rescue & Redistribution Network**

This repository contains the backend API for FoodBridge, built with Django and Django REST Framework (DRF). It provides functionality for user registration, authentication, donation management, and donation claiming with role-based permissions.

---

## 🗂 Table of Contents

1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)
3. [Models](#models)
4. [Serializers](#serializers)
5. [Views & Endpoints](#views--endpoints)
6. [Authentication](#authentication)
7. [User Roles](#user-roles)
8. [Testing](#testing)
9. [Next Steps](#next-steps)

---

## Project Overview

FoodBridge connects individuals willing to donate surplus food (Donors) with people in need (Receivers). The backend API allows:

* **User registration** with role selection
* **JWT-based authentication**
* **Create, read, update, delete** (CRUD) operations for donations by Donors
* **Claiming donations** by Receivers
* **Role-based permissions** to enforce access control

---

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone git@github.com:ishworii/Foodbridge_backend.git
   cd Foodbridge-backend
   ```
2. **Create virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Apply migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **Run development server**

   ```bash
   python manage.py runserver
   ```
5. **Access API** at `http://localhost:8000/api/`

---

## Models

### Profile

* **Fields:**

  * `user` — OneToOne to `User`
  * `role` — Choice of `donor` or `receiver`

### Donation

* **Fields:**

  * `donor` — ForeignKey to `User`
  * `title` — CharField
  * `description` — TextField
  * `quantity` — PositiveIntegerField
  * `location` — CharField
  * `is_claimed` — BooleanField
  * `claimed_by` — ForeignKey to `User` (nullable)
  * `created_at` — DateTimeField (auto\_now\_add)

---

## Serializers

* **RegisterSerializer**

  * Handles user creation and assigns `role` to the Profile
* **DonationSerializer**

  * Serializes all fields of `Donation`
  * Read-only: `id`, `donor`, `created_at`, `claimed_by`, `is_claimed`

---

## Views & Endpoints

### Registration

* `POST /api/register/`

  * **Payload:** `{ "username", "email", "password", "role" }`

### Authentication (JWT)

* `POST /api/token/` — Obtain access & refresh tokens
* `POST /api/token/refresh/` — Refresh access token

### Donation CRUD

* `GET    /api/donations/` — List donations
* `POST   /api/donations/` — Create a donation (Donor only)
* `GET    /api/donations/{id}/` — Retrieve a donation
* `PUT    /api/donations/{id}/` — Full update (Donor only)
* `PATCH  /api/donations/{id}/` — Partial update (Donor only)
* `DELETE /api/donations/{id}/` — Delete (Donor only)

### Claim Donation

* `POST /api/donations/{id}/claim/` — Claim a donation (Receiver only)

---

## Authentication

* Uses **Simple JWT**
* Default token lifetimes configured in `settings.py`
* Add header:

  ```
  Authorization: Bearer <access_token>
  ```

---

## User Roles

* **Donor**

  * Can register donations
  * Can view all donations
* **Receiver**

  * Can view all donations
  * Can claim unclaimed donations

Permissions enforced via custom DRF permission classes (`IsDonor`, `IsReceiver`).

---

## Testing

1. **Register users** with roles
2. **Login** to obtain JWT tokens
3. **Create donations** as Donor
4. **Attempt unauthorized actions** (e.g., Receiver creating donation)
5. **Claim donation** as Receiver
6. **Verify double-claim protection**
7. **List and filter** donations

---

## Next Steps

* Add filtering and search (e.g., by location or `is_claimed` status)
* Implement pagination
* Add profile editing endpoints
* Set up email notifications
* Build the frontend to consume these APIs

