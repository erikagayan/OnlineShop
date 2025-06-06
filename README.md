# Online-Shop v2.0

## Features
In the online shop API service, you can create categories, further create products by selecting them categories, as well as add products to the cart, specifying the quantity you need (if such quantity is in stock). Also admin can appoint a manager and moderator, who will manage the goods and users.

The user management functionality is handled by a separate microservice built with Django and Django REST Framework. This microservice includes functionalities for user creation, authentication using JWT, and user management.

The application also has an interface written using React and Typescript



## Installation
1. **Clone the repository:**
    ```bash
    git clone https://github.com/erikagayan/OnlineShop.git
    cd OnlineShop
    ```
2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```
4. **Create a `.env` file in the project root and add the following variables:**

    ```dotenv
    SECRET_KEY=your_secret_key
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=localhost
    DB_PORT=5432
    ```
5. **Apply migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6. **Start Redis container:**

    ```bash
    docker run -d --name redis -p 6379:6379 redis
    ```
7. **Create a superuser for accessing the admin interface:**

    ```bash
    python manage.py createsuperuser
    ```
8. **Start the development server:**

    ```bash
    python manage.py runserver
    ```



## Permission:
### Admin:
- Create moderators
- Create managers
- Add products
- Modify
- Delete
- Update

## Moderator:
- Create moderators
- Add products
- Modify
- Delete
- Update

### Manager:
- Add products
- Modify
- Delete
- Update

### Customer:
- View Products

## Technologies:
- Django
- React
- PostgreSQL
- SwaggerUI
- Redis
- Docker