
# Rule Engine Application
The Rule Engine Application is a powerful, web-based platform that enables users to create, evaluate, modify, combine, and manage complex rules through a user-friendly interface. Designed with security and robust functionality in mind, this application is ideal for decision-making processes, automated workflows, and any scenario requiring advanced conditional logic.
With a secure user authentication system, users can create accounts, log in, and reset passwords, with rules stored in an SQLite database for easy access and modification. The Rule Engine supports complex rule creation by parsing expressions into an Abstract Syntax Tree (AST) for structured evaluation. Users can combine multiple rules to form intricate logical expressions, making it ideal for dynamic workflows.

## Web Server URL
https://e301-2405-201-e02c-a24c-7037-7bc0-1601-3060.ngrok-free.app/login



![Rule1](https://github.com/user-attachments/assets/6975a149-f7f3-4c91-bb2f-58fc84051634)
![rule2](https://github.com/user-attachments/assets/84ed8163-0ef7-4652-937d-f8b0a78320ce)
![rule3](https://github.com/user-attachments/assets/ee0c770c-64d1-4210-bf98-1121fc1cbcf8)
![rule4](https://github.com/user-attachments/assets/272cfef3-659c-4f60-94b0-83c3bbb4a544)
## Features
User Registration and Login: Secure user accounts with hashed passwords, session management, and authentication.
Password Reset Functionality: Users can reset forgotten passwords via email verification.
Rule Creation, Combination, and Evaluation: Users can create, modify, combine, or delete rules with support for logical operators like AND, OR, and various comparison operators.
Error Handling: Graceful handling of errors, including invalid input data, database errors, and missing user input.
User-Friendly Web Interface: Clean HTML/CSS front-end for a smooth user experience.

## Technologies Used
Flask: Backend framework for web request handling and authentication.
SQLite: Lightweight database for storing user information and rule data.
Flask-Mail: For sending password reset emails.
Werkzeug: Provides secure password hashing.
HTML/CSS: Used for building a clean and interactive front-end interface.

## Installation

## Prerequisites
```sh
Python 3.6 or higher
pip (Python package installer) 
```

# Step-by-Step Installation

## 1.Clone the Repository:
```sh
git clone https://github.com/yourusername/RuleEngine.git
cd rule-evaluation-app
```

## 2.Create a Virtual Environment (Recommended):

```sh
python -m venv venv

source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
## 3.Install Required Dependencies:

```sh
pip install -r requirements.txt
```
## 4.Set Up Environment Variables:

Create a .env file in the root directory and add your email credentials:

```sh
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
```

## 5.Initialize the Database:

The database will initialize automatically the first time the application is run. To manually set it up, use:
```sh
python init_db.py
```
## 6.Run the Application:

```sh
python app.py
```
Access the application at http://127.0.0.1:5000/.

# Application Architecture

## Database Schema
-Users Table: Stores user credentials, including username, hashed password, and email.**
-Rules Table: Saves rules in a structured format, allowing for evaluation, modification, and combination.**

## Rule Evaluation and Combination Logic
**Rule Parsing with AST: The rules are parsed into an Abstract Syntax Tree (AST) to systematically evaluate and structure rules, allowing users to build complex conditional expressions.**
**Combining Rules: Users can combine rules using logical operators (AND, OR). The system supports nested expressions and allows for combinations that create advanced workflows. Rules can be combined by creating a new rule that references existing ones, making them adaptable and modular.**

## Error Handling
The application has comprehensive error handling to ensure smooth and secure operation:

-Invalid Input: Provides meaningful feedback to users when invalid data is entered, such as incorrect data types or unsupported expressions.

-Database Errors: Handles database connectivity issues and raises alerts for potential data storage problems.

-User Input Validation: Ensures all required fields are filled and valid, preventing unexpected behavior.

-Rule Syntax Checking: Validates rule syntax before saving or combining, alerting users to syntax issues.

## User Authentication and Security

-Session Management: User sessions are tracked with Flask’s session management to ensure security.
-Password Hashing: Utilizes Werkzeug for secure password hashing to protect user data.
-Email Integration: Sends password reset emails with Flask-Mail to streamline password recovery.

## Dependencies

###Install dependencies with:

`pip install Flask Flask-Mail Werkzeug python-dotenv`

##Running with Docker (Optional)

Steps to Run with Docker

####Create a Dockerfile:

```sh
`FROM python:3.8-slim`

`WORKDIR /app`

`COPY requirements.txt .`
`RUN pip install --no-cache-dir -r requirements.txt`

COPY . .

CMD ["python", "app.py"]
```
###Create a docker-compose.yml File:  
```sh
#version: '3'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - MAIL_USERNAME=your_email@gmail.com
      - MAIL_PASSWORD=your_email_password
	  
	  ```
	  
###Build and Run the Container:


```sh 
docker-compose up --build
```

##HTML Files

The application includes various HTML files for user interaction:

-login.html: Login page for user authentication.
-register.html: Registration page for new users.
-forgot_password.html: Password reset request page.
-reset_password.html: Password reset page.
-index.html: Main page for rule evaluation and interaction.
-user.html: User profile and account management.

#Contributing

We welcome contributions to expand the Rule Engine Application’s features and capabilities. Please submit pull requests or open issues with suggestions or feedback.


