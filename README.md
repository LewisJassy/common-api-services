# API Repo

A collection of reusable, versioned APIs for common functionalities such as authentication, user management, and payment integrations. These APIs are framework-agnostic and are packaged as a Python library, which can be easily installed and used across multiple projects.

## Table of Contents
- [API Repo](#api-repo)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Integrating with Frameworks](#integrating-with-frameworks)
      - [Flask Integration](#flask-integration)
      - [Django Integration](#django-integration)
  - [API Documentation](#api-documentation)
    - [Authentication API](#authentication-api)
    - [User API](#user-api)
    - [Payment API](#payment-api)
    - [Utilities](#utilities)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Features
- **Reusable APIs**: Authentication, User management, Payment integration.
- **Framework-Agnostic**: Works with any web framework (Flask, Django, etc.).
- **Versioning**: APIs are versioned (e.g., v1/), ensuring backward compatibility.
- **Docker Support**: Optionally containerized for easier deployment.
- **Package Installation**: Easy installation via pip and integration into new projects.

## Getting Started

### Installation
Install the package via pip from the Python Package Index (PyPI) or directly from the repository:

```bash
pip install api-repo
```

Alternatively, you can install it from the GitHub repository for development purposes:

```bash
pip install git+https://github.com/your-username/api-repo.git
```

### Usage
Once installed, you can import the APIs directly into your project:

```python
from api_repo.v1.auth import authenticate_user
from api_repo.v1.user import create_user
```

You can use these APIs in your project just like any other Python module. The APIs are independent of any web framework but have specific integration points for Flask and Django.

### Integrating with Frameworks

#### Flask Integration
Install Flask:

```bash
pip install flask
```

In your Flask project, import the necessary API and set up routes:

```python
from flask import Flask
from api_repo.v1.auth import authenticate_user

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
        return authenticate_user()

if __name__ == '__main__':
        app.run()
```

#### Django Integration
Install Django:

```bash
pip install django
```

In your Django project, import the API and set up URLs:

```python
from django.urls import path
from api_repo.v1.auth import authenticate_user

urlpatterns = [
        path('login/', authenticate_user, name='login'),
]
```

## API Documentation

### Authentication API
- **Login**: Authenticate a user with username and password.
- **Register**: Create a new user with email and password.
- **OAuth Integration**: OAuth authentication for third-party logins.

Example Usage:

```python
from api_repo.v1.auth import authenticate_user

# POST request to authenticate a user
authenticate_user(username="testuser", password="password123")
```

### User API
- **Create User**: Add a new user to the system.
- **Get User**: Retrieve user details by ID.
- **Update User**: Modify user information.
- **Delete User**: Remove a user from the system.

Example Usage:

```python
from api_repo.v1.user import create_user, get_user

# Create a new user
create_user(email="test@example.com", password="password123")

# Get user details
get_user(user_id=1)
```

### Payment API
- **Process Payment**: Handle payments via third-party services (Stripe, PayPal, etc.).
- **Refund Payment**: Initiate a refund for a payment.

Example Usage:

```python
from api_repo.v1.payment import process_payment

# Process a payment
process_payment(amount=100.0, payment_method="credit_card")
```

### Utilities
- **Logging**: Standardized logging for debugging and tracking.
- **Validation**: Helper functions for validating inputs.

## Testing
Unit tests are provided for all APIs to ensure their functionality and correctness.

Run the tests:

```bash
pytest
```

You can find the test cases in the `tests/` folder. Tests are organized by API (test_auth.py, test_user.py, etc.).

## Contributing
We welcome contributions to this repo. If you’d like to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add feature'`).
4. Push to your branch (`git push origin feature-name`).
5. Create a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.