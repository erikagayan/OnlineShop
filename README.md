# Online-Shop v2.0

## Features
In the online shop API service, you can create categories, further create products by selecting them categories, as well as add products to the cart, specifying the quantity you need (if such quantity is in stock). Also admin can appoint a manager and moderator, who will manage the goods and users.

The user management functionality is handled by a separate microservice built with Django and Django REST Framework. This microservice includes functionalities for user creation, authentication using JWT, and user management.

The application also has an interface written using React and Typescript

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