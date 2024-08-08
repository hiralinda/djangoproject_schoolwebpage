# Teacher-Student Django Platform

## Video Preview

[Video Link](https://youtu.be/Qk2ap_J89tg)

## Description

This project is a comprehensive language school website built using Django, designed to facilitate the interaction between teachers and students. It was created as the [Final Project](https://cs50.harvard.edu/web/2020/projects/final/capstone/) for CS50's Web Programming with Python and JavaScript course. The platform offers distinct features for both user types, creating a seamless and efficient educational environment. 

### Features

- User Registration and Authentication
- User Types: Users can register as either students or teachers.
- Authentication: Secure login and logout functionality using Django's authentication system.

## Setup and Deployment

### Installation

This project was developed in Python version `3.10.5`.

Clone the Repository: `git clone <repository-url>`

Navigate to the Project Directory: ```cd teacher-student-django-platform```

Install Dependencies: ```pip install -r requirements.txt```

Configure Google API: Obtain credentials from Google Cloud Console and save them as credentials.json in the project directory.

Apply Migrations: ```python manage.py migrate```

Run the Development Server: ```python manage.py runserver```

### Usage

+ Register as a Student or Teacher.
+ Update Your Profile with relevant information.
+ Browse Teacher Profiles (if logged in as a student).
+ Contact Teachers and start conversations.
+ Schedule Classes using Google Meet (if logged in as a teacher).
+ This platform aims to streamline the process of language learning by providing an easy-to-use interface for both students and teachers, ensuring effective communication and scheduling of lessons.

### User Profiles

- Teacher Profiles: Teachers can update their profiles, including their bio and schedule.
- Student Profiles: Students can update their profiles and browse through teacher profiles.

### Teacher Functionality

- Profile Management: Teachers can manage their personal information and availability.
- Inbox: Teachers can communicate with students who have contacted them.
- Class Scheduling: Teachers can schedule classes via Google Meet integration, allowing for easy and efficient online lessons.
- Upcoming classes: Teachers can access a list of upcoming scheduled classes and easily access the Google Meets Link generated.

### Student Functionality

- Profile Management: Students can manage their personal information
- Browse Teachers: Students can browse through the list of teachers, view their profiles, and contact them for lessons.
- Inbox: Students can message teachers and keep track of their conversations.
- Upcoming classes: Students can access a list of upcoming scheduled classes and easily access the Google Meets Link generated.

### Messaging System

- Two-Way Communication: A built-in inbox feature allows students to initiate conversations with teachers. Teachers can respond to these messages.
- Real-Time Chat: Messages are displayed in a chat-like interface for easy communication.

### Google Calendar Integration

- Class Scheduling: Teachers can schedule classes with students using Google Calendar integration, making it easy to set up and manage online classes via Google Meet.

## Distinctiveness and Complexity:

This project stands out by offering tailored functionalities specifically designed for students and teachers in a language school setting. The platform's index page highlights how it works and showcases its features, emphasizing the unique benefits it offers. The custom user model (CustomUser) differentiates roles, providing personalized experiences for both students and teachers. Integrating Google Calendar for scheduling streamlines the process, allowing teachers to manage their availability and generate Google Meet links for classes. The messaging system enhances communication, enabling students and teachers to interact seamlessly.

In terms of complexity, the project handles intricate data relationships between users and profiles, manages OAuth 2.0 authentication for Google Calendar integration, and ensures message handling. The use of Tailwind CSS, SASS, and JavaScript for a responsive UI adds to the technical depth, requiring robust error handling and debugging to maintain a smooth user experience. The index page effectively presents the advantages of signing up, highlighting how teachers' profiles become visible on the front page, allowing students to browse and contact them for classes. Teachers can then schedule classes with new students, generating Google Meet links for chosen times and dates. This information, along with the Meet links, is displayed in the 'upcoming classes' section, accessible to both teachers and students for easy class access.

For students, signing up allows them to browse through the profiles of signed-up teachers, choose the one that best fits their criteria, and initiate contact to express interest in classes and request scheduling. This interactivity and the ability to manage availability and communication seamlessly create a distinct and engaging platform for language learning.

## File Structure

```
├── djangoproject/
│   └── settings.py
├── hira/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── sass/
│   └── templates/
│       ├── hira/
│       │   ├── availability.html
│       │   ├── browse_teachers.html
│       │   ├── edit_profile.html
│       │   ├── home.html
│       │   ├── inbox.html
│       │   ├── index.html
│       │   ├── layout.html
│       │   ├── profile.html
│       │   ├── schedule_class.html
│       │   └── scheduled_classes.html
│       └── registration/
│           ├── login.html
│           └── signup.html
├── media/
│   └── profile_pics/
├── credentials.yaml
├── db.sqlite3
└── requirements.txt
```
<sub>generated by https://tree.nathanfriend.io/</sub>

```djangoproject/```
+ ```settings.py``` Contains the settings for the Django project, including configurations for installed apps, middleware, databases, static files, and more.

```hira/```
+ ```static/``` This directory contains static files used in the project.

    + ```css/ ```Contains CSS files for styling the application.

    + ```js/ ```Contains JavaScript files for client-side functionality.

    + ```sass/ ```Contains SCSS (Sass) files for pre-compiled stylesheets.

+ ```templates/ ```Contains HTML templates for rendering views.

    + ```hira/``` Contains the main templates used by the hira app.
        
        + ```availability.html``` Template for displaying and managing teacher availability.
        + ```browse_teachers.html ```Template for browsing through teacher profiles.
        + ```edit_profile.html``` Template for editing user profile information.
        + ```home.html``` Template for student or teacher dashboard page, displaying edit profile, inbox, and upcoming classes option.
        + ```inbox.html``` Template for the messaging inbox where students and teachers can communicate.
        + ```index.html``` The landing page of the website, explaining the platform’s features and benefits.
        + ```layout.html``` Base template used to provide a consistent header and footer across other templates.
        + ```profile.html``` Template for displaying individual teacher or student profiles.
        + ```schedule_class.html``` Template for scheduling new classes with a student through Google Calendar/ Meets API.
        + ```scheduled_classes.html ```Template for viewing upcoming scheduled classes and access the Google Meets Link generated.
    + ```registration/``` Contains templates related to user authentication.
        + ```login.html``` Template for user login.
        + ```signup.html``` Template for user registration/sign-up.

```media/```
+ ```profile_pics/``` Directory for storing user profile pictures uploaded by users.

```credentials.yaml``` Contains sensitive credentials needed for external integrations (Google Calendar API credentials). 

```db.sqlite3``` SQLite database file where Django stores data for the project. It contains all the application's models and their data.

```requirements.txt``` Lists all the Python packages and their versions required to run the project. This file is used to install dependencies with pip.

## Additional Information 

Some potential features that I would like to implement on the project to improve it include:

- Have the users choose their language of interest on their profile
- Filter available teachers based on the language they teach;
- Display the upcoming classes on a calendar-looking interface;
- Edit and delete scheduled classes;
- Inbox notification;
- Pagination on browse teachers page and upcoming classes page;
- Dark mode;

---

*[This project](https://cs50.harvard.edu/web/2020/projects/final/capstone/) was my Final Project for the CS50 Web Programming with Python and JavaScript course.*