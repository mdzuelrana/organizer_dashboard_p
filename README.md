# 🎉 Event Management System

A professional full-stack Event Management System built with Django, PostgreSQL, Tailwind CSS, and JavaScript. This project was developed as a final full-stack web development project to demonstrate real-world application architecture, authentication systems, role-based access control, and event management workflows.

---

# 🚀 Features


## 🔐 Authentication System
- User Registration
- Email Verification
- Secure Login & Logout
- Password Reset
- Password Change
- Django Authentication System

---


# 👥 Role-Based Access Control

The system supports three user roles:


## Admin
- Manage all users
- Assign groups & roles
- Monitor events
- Control permissions


## Organizer
- Create Events
- Update Events
- Manage Participants
- Handle RSVPs


## Participant
- Browse Events
- RSVP to Events
- Manage Personal Profile

---


# 📅 Event Features

- Event Creation & Management
- RSVP System
- Event Details Page
- Participant Management
- Responsive Event Dashboard

---


# 👤 Profile Management

- Update Profile Information
- Upload Profile Image
- Change Password
- Secure User Settings

---


# 🎨 Responsive UI

Built using Tailwind CSS with a modern and mobile-friendly design.

---


# 🛠️ Technologies Used

## Backend
- Django
- Django Authentication & Authorization
- Django Class-Based Views
- PostgreSQL

## Frontend
- HTML
- Tailwind CSS
- JavaScript

---


# 📁 Project Structure

```bash
event-management-system/
│
├── accounts/
├── events/
├── participants/
├── templates/
├── static/
├── media/
│
├── event_management/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── requirements.txt

⚙️ Installation

Clone Repository
git clone <repository_url>
cd event-management-system

🐍 Create Virtual Environment
Windows
python -m venv venv
source venv/Scripts/activate
Linux/Mac
python3 -m venv venv
source venv/bin/activate

📦 Install Dependencies
pip install -r requirements.txt
🗄️ Configure Database

Update your PostgreSQL database credentials in:

settings.py

Example:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'event_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

🔄 Run Migrations

python manage.py makemigrations
python manage.py migrate
👤 Create Superuser
python manage.py createsuperuser

▶️ Run Development Server

python manage.py runserver

🌐 Application Flow

User Registration
        ↓
Email Verification
        ↓
Secure Login
        ↓
Role-Based Dashboard
        ↓
Event Management & RSVP

📚 What I Learned

This project improved my understanding of:

Authentication Systems
Role-Based Permission Control
Django Class-Based Views
PostgreSQL Database Management
Full-Stack Web Development
Real-World Project Structure
Responsive UI Design

👨‍💻 Author

Developed by Md Zuel Rana

📄 License

This project is licensed under the MIT License.
