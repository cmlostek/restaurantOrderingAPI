A FastAPI-based project for managing a restaurant's operations: menus, ingredients, orders, payments, promotions, and customer reviews. The database is dropped, recreated, and automatically populated on each application start from JSON seed files.

---

## **Table of Contents**

1. [Overview](#overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Getting Started](#getting-started)
    1. [Prerequisites](#prerequisites)
    2. [Installation](#installation)
    3. [Configuration](#configuration)
5. [Database Seeding](#database-seeding)
6. [Running the Application](#running-the-application)
7. [API Endpoints](#api-endpoints)
8. [Testing](#testing)
9. [Project Structure](#project-structure)
10. [Contributing](#contributing)


---

## **Overview**

This API serves as the backend for an online restaurant ordering system. It allows:

- **Menu management** with dish definitions and ingredient associations
- **Inventory tracking** of resources (ingredients)
- **Order processing** for registered users and guests
- **Payment recording** and optional promotions
- **Order detail** items (e.g., special instructions)
- **Customer reviews** linked to orders
- **Revenue reporting** by date

Data is persisted in a MySQL database through SQLAlchemy, with Pydantic schemas enforcing payload and response models.

---

## **Work in Progress**

The following features are currently being developed or planned for future releases:

- **Resource Management in Dashboard:**
  - Add, edit, and remove resources (ingredients) directly from the admin dashboard for easier inventory control.
- **Customer Points / Loyalty System:**
  - Implement a points or rewards system for customers based on their order history.
  - Allow customers to redeem points for discounts or special offers.
- **Review System Enhancements:**
  - Enable customers to leave reviews for dishes and orders.
  - Display reviews and ratings on the customer dashboard and menu pages.
- **Improved Admin & Customer Dashboards:**
  - More analytics, order history, and management tools for admins.
  - Enhanced order tracking and personalized recommendations for customers.
- **UI/UX Improvements:**
  - Ongoing improvements to the frontend for a smoother and more intuitive user experience.

If you have suggestions or want to contribute to these features, please see the [Contributing](#contributing) section below.

---

## **Features**

- Full **CRUD** operations on all entities: Users, Menu, Resources, Orders, OrderDetails, Payments, Promotions, Reviews,  etc
- **Many-to-many** relationship between Menu and Resources (ingredients)
- Automatic database reset & seeding on startup.
- Interactive API documentation (Swagger UI & ReDoc)
- Daily revenue summary endpoint
- Comprehensive, independent **pytest** test suite

---

## **Technology Stack**

- **Python 3.9+**
- **FastAPI** (API framework)
- **SQLAlchemy** (ORM)
- **Pydantic** (data validation)
- **Uvicorn** (server)
- **MySQL** (database)
- **Pytest** (unit testing)

---
## **Getting Started**


### **Prerequisites**

- Python 3.9 or later
- MySQL server & database (e.g. restaurant_api)
- Git


### **Installation**

1. **Clone the repository**

```bash
git clone https://github.com/cmlostek/itsc3155_GroupProject.git
cd api
```

1. **Create and activate** a virtual environment

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
**On Windows:**
```bash
cd itsc3155_GroupProject/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. **Install dependencies**

```
pip install -r requirements.txt
```
  

### **Configuration**

  

Edit the database URL in api/dependencies/config.py:

```Python
class conf:  
    db_host = "localhost"  
    db_name = "your_database_name"  
    db_port = 3306  
    db_user = "root"  
    db_password = "your_database_password"  
    app_host = "localhost"  
    app_port = 8000
```


---

## **Database Seeding**

  

On each application startup, the database tables are:

1. Dropped2. Recreated
2. Seeded in this order from api/data/*.json:

    - Users
    - Menu
    - Resources (ingredients)
    - Menu ↔ Resources links through backtracking.
    - Orders
    - Promotions
    - Payments
    - OrderDetails 
    - Reviews
    
No additional migration or manual seeding steps are required.

---

## **Running the Application**

```
uvicorn api.main:app --reload
```

- **Swagger UI**:  http://127.0.0.1:8000/docs
- **ReDoc**:       http://127.0.0.1:8000/redoc
    
---

## **Running the Frontend**

The frontend is a React app located in `frontend/react-ts-frontend`.

### **Prerequisites**
- [Node.js](https://nodejs.org/) (v16 or later recommended)

### **Steps**
1. Open a new terminal window.
2. Change directory to the frontend folder:
   ```
   cd frontend/react-ts-frontend
   ```
3. Install dependencies:
   ```
   npm install
   ```
4. Start the development server:
   ```
   npm run dev
   ```
5. The app will be available at the URL printed in the terminal (typically http://localhost:5173/).

---

## **API Endpoints**


### **Users**

|**Method**|**Path**|**Description**|
|---|---|---|
|GET|/users/|List all users|
|GET|/users/{id}|Retrieve a specific user|
|POST|/users/|Create a new user|
|PUT|/users/{id}|Update an existing user|
|DELETE|/users/{id}|Delete a user|

### **Menu**

| **Method** | **Path**        | **Description**                     |
| ---------- | --------------- | ----------------------------------- |
| GET        | /menu/          | List all dishes                     |
| GET        | /menu/{dish_id} | Retrieve a specific dish            |
| POST       | /menu/          | Create a dish (with ingredient IDs) |
| PUT        | /menu/{dish_id} | Update a dish and its ingredients   |
| DELETE     | /menu/{dish_id} | Delete a dish                       |

### **Resources (Ingredients)**

|**Method**|**Path**|**Description**|
|---|---|---|
|GET|/resources/|List all resources|
|GET|/resources/{resource_id}|Retrieve a resource|
|POST|/resources/|Create a resource|
|PUT|/resources/{resource_id}|Update a resource|
|DELETE|/resources/{resource_id}|Delete a resource|

### **Promotions**

|**Method**|**Path**|**Description**|
|---|---|---|
|GET|/promotions/|List all promotions|
|GET|/promotions/{promotion_id}|Retrieve a promotion|
|POST|/promotions/|Create a promotion|
|PUT|/promotions/{promotion_id}|Update a promotion|
|DELETE|/promotions/{promotion_id}|Delete a promotion|

### **Payments**

|**Method**|**Path**|**Description**|
|---|---|---|
|GET|/payments/|List all payments|
|GET|/payments/{payment_id}|Retrieve a payment|
|POST|/payments/|Create a payment|
|PUT|/payments/{payment_id}|Update a payment|
|DELETE|/payments/{payment_id}|Delete a payment|

### **Orders**

|**Method**|**Path**|**Description**|
|---|---|---|
|GET|/orders/|List all orders|
|GET|/orders/{order_id}|Retrieve a specific order|
|POST|/orders/|Create a new order|
|PUT|/orders/{order_id}|Update an existing order|
|DELETE|/orders/{order_id}|Delete an order|
|GET|/orders/by-range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD|List orders within date range|

### **Order Details**

| **Method** | **Path**                               | **Description**                                   |
| ---------- | -------------------------------------- | ------------------------------------------------- |
| GET        | /orders/{order_id}/details/            | List all details for an order                     |
| GET        | /orders/{order_id}/details/{detail_id} | Retrieve one detail line                          |
| POST       | /orders/{order_id}/details/            | Create a new detail line                          |
| PUT        | /orders/{order_id}/details/{detail_id} | Update a detail line                              |
| DELETE     | /orders/{order_id}/details/{detail_id} | Delete a detail line                              |
| DELETE     | /orders/{order_id}/details             | Deletes all order details under a single order id |

### **Reviews**

|**Method**|**Path**|**Description**|
|---|---|---|
|GET|/users/{user_id}/reviews/|List reviews for a user|
|GET|/reviews/{review_id}?user_id={user_id}|Retrieve a specific review|
|POST|/reviews/?user_id={user_id}|Create a review for a user|
|PUT|/reviews/{review_id}?user_id={user_id}|Update a review|
|DELETE|/reviews/{review_id}?user_id={user_id}|Delete a review|

### **Reports**

| **Method** | **Path**                      | **Description**                         |
| ---------- | ----------------------------- | --------------------------------------- |
| GET        | /reports/revenue/{YYYY-MM-DD} | Total revenue generated on a given date |


---
## **Testing**

  
All endpoints are covered by pytest with a feature that resets and reseeds the database before each test.
- Run all tests:

```
pytest 
```

- Run specific file:

```
pytest tests/test_menu.py
```

  
---

## **Project Structure**

```
.
├── api/
│   ├── data/              # JSON files for database
│   ├── dependencies/      # DB setup & startup logic
│   ├── models/            # SQLAlchemy ORM classes
│   ├── schemas/           # Pydantic request & response models
│   ├── controllers/       # logical functions for routes
│   ├── routers/           # FastAPI route definitions
│   └── main.py            # Application entry point
├── frontend/
│   └── react-ts-frontend/
│       ├── src/           # React source code
│       ├── public/        # Static assets
│       ├── package.json   # Frontend dependencies
│       └── ...            # Other frontend files
├── tests/                 # pytest modules & fixtures
├── seed.py                # Manual seeder script to add items to database 
├── requirements.txt       # needed python dependencies 
└── README.md
```


---

## **Contributing**

1. Fork the repository
2. Create a feature or bugfix branch
3. Implement and test your changes
4. Submit a pull request

Please follow the existing code style and update tests where appropriate.



