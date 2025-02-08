# Kalakar

Kalakar is a Django-based e-learning platform designed to provide a seamless and interactive learning experience. This platform allows educators to create and manage courses, while students can enroll and participate in various learning activities.

## Features

- User authentication and authorization
- Course creation and management
- Enrollment and progress tracking
- Responsive design for mobile and desktop

## Getting Started

This guide helps you set up a development environment for this project.

## Prerequisites

- **Python:** 3.8 or higher. Check your version: `python --version`.
  - Download and install Python from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

## Setting Up the Development Environment

1. **Create and Activate a Virtual Environment:**

    - Use a virtual environment to isolate project dependencies:
        ```bash
        python -m venv venv
        source venv/bin/activate  # For Linux/macOS
        venv\Scripts\activate.bat  # For Windows
        ```

2. **Install Required Packages:**

    - Activate your virtual environment and install dependencies:
        ```bash
        pip install -r dev-requirements.txt
        ```

    - **Linux:** Install additional packages for MySQL support:
        ```bash
        sudo apt install libmysqlclient-dev default-libmysqlclient-dev pkg-config python3-dev build-essential
        ```
        (Adjust the command for your Linux package manager)

3. **Install Pre-commit Hooks:**

    - Maintain code quality with pre-commit hooks:
        ```bash
        pre-commit install --install-hooks
        ```

4. **Configure the Environment:**

    - Rename `.env.example` to `.env` and update variables with your database credentials and other values.
    - Supported databases: [https://docs.djangoproject.com/en/5.1/ref/databases/](https://docs.djangoproject.com/en/5.1/ref/databases/)

5. **Apply Database Migrations:**

    - Create and apply database migrations:
        ```bash
        python manage.py makemigrations
        python manage.py migrate
        ```

6. **Start the Development Server:**

    - Start the development server:
        ```bash
        python manage.py runserver
        ```
