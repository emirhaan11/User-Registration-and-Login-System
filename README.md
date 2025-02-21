# User Registration and Login System

This is a **User Registration and Login System** built with Python and Tkinter. It allows users to register, log in, and manage their profiles with profile pictures. The system also includes an admin panel and email notifications for new registrations.

## Features

- **User Registration**: Users can sign up with their personal details, including name, surname, email, age, department, and gender.
- **Profile Pictures**: Users can upload their profile pictures, stored as binary data in an SQLite database.
- **Login System**: Users can log in using their username and password.
- **Admin Panel**: Admin can access the user database.
- **Email Notification**: New users receive an email with their login credentials.
- **Secure Data Storage**: User data is stored in an SQLite database.

## Installation

### Prerequisites
Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).


### Clone the Repository
```sh
git clone https://github.com/your-username/user-login-system.git
cd user-login-system
```

### Install Required Packages
Use the following command to install the necessary dependencies:
```sh
pip install -r requirements.txt
```

### Environment Variables
Create a **.env** file in the project directory and add your email credentials for sending user registration emails:
```env
EMAIL_SENDER="your-email@gmail.com"
EMAIL_PASSWORD="your-email-password"
```
> **Note:** You may need to enable "Less secure apps" in your email settings or generate an app password.

## Usage

### Running the Application
Run the following command to start the application:
```sh
python main.py
```

### Registering a User
1. Click the **REGISTER** button.
2. Fill in the required details and upload a profile picture.
3. Click **SAVE** to register.
4. You will receive an email with your username and password.

### Logging In
1. Enter your **username** and **password**.
2. Click **LOGIN** to access your profile.

### Admin Access
- Log in with the credentials:
  ```
  Username: admin
  Password: admin.
  ```
- The user database file (USERS_INFO.db) will open.

## Database Structure
The application uses SQLite for storing user information. The **USERS_INFO** table has the following fields:
- `name` (TEXT)
- `surname` (TEXT)
- `e_mail` (TEXT)
- `age` (INT)
- `department` (TEXT)
- `sex` (TEXT)
- `image` (BLOB)
- `password` (INT)
- `user_name` (TEXT)


