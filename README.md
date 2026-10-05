=>Doctor Appointment System

The Doctor Appointment System is a full-stack healthcare appointment management application developed using Flutter, Django, and MySQL. The system is designed to simplify the process of finding doctors, viewing their schedules, booking appointments, and managing communication between users, doctors, and administrators.

=>User Module

Users can register and log in to the application, view available doctors, check their specialization, qualification, and experience, and view doctor schedules. Users can book appointments by selecting the available date and time. They can also view, update, and cancel their appointments. Additional features include submitting doctor ratings, complaints, and feedback, as well as viewing replies and ratings.

=>Doctor Module

Doctors can register through the system and access their account after administrator approval. Doctors can manage their schedules by adding, viewing, editing, and deleting schedules. They can view appointments booked by users and accept or reject appointments. Doctors can also view ratings submitted by users.

=>Admin Module

Administrators can manage the complete system through the admin module. The admin can view and manage doctors and users, approve or reject doctor registrations, view and reply to user complaints, view feedback, and access system reports.

=>Technologies Used

.User/Patient Frontend: Flutter, Dart

.Doctor Frontend: HTML, CSS, Bootstrap, Django Templates

.Admin Frontend: HTML, CSS, Bootstrap, Django Templates

.Backend: Python, Django

.Database: MySQL

.Development Tools: Android Studio, Visual Studio Code, SQLyog, Git, GitHub

=>System Architecture

The system consists of three main modules: User, Doctor, and Admin. The User/Patient module is developed using Flutter and Dart and communicates with the Django backend through HTTP requests and APIs. The Doctor and Admin modules are web-based interfaces developed using HTML, CSS, Bootstrap, and Django Templates. These modules are handled directly by the Django application.

Django manages authentication, business logic, database operations, doctor schedules, appointments, ratings, complaints, feedback, and admin management. MySQL is used as the database.

Architecture:

User/Patient
Flutter / Dart
↓
Django APIs
↓
MySQL

Doctor
HTML / CSS / Bootstrap / Django Templates
↓
Django
↓
MySQL

Admin
HTML / CSS / Bootstrap / Django Templates
↓
Django
↓
MySQL

Main Features

*User Registration and Login

*Doctor Registration and Approval

*Doctor Search and Details

*Doctor Schedule Management

*Appointment Booking

*Appointment Update and Cancellation

*Appointment Accept/Reject

*Doctor Ratings

*Complaint and Reply System

*User Feedback

*Admin Management

*Reports

*Logout and Session Management

The project was developed to provide a simple and organized platform for online doctor appointment management, reducing manual appointment processes and making doctor and appointment information easily accessible to users.
