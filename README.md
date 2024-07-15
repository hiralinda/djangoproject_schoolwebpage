# TEACHER-STUDENT DJANGO PLATFORM 

### Video Demo:  <URL HERE>

## Description:

This project is a comprehensive language school website built using Django, designed to facilitate the interaction between teachers and students. It was created as the Final Project for CS50's Web Programming with Python and JavaScript course. The platform offers distinct features for both user types, creating a seamless and efficient educational environment. Here is a detailed overview of the project:

### Features
- User Registration and Authentication
* User Types: Users can register as either students or teachers.
+ Authentication: Secure login and logout functionality using Django's authentication system.

### User Profiles
- Teacher Profiles: Teachers can update their profiles, including their bio and schedule.
* Student Profiles: Students can update their profiles and browse through teacher profiles.

### Teacher Functionality
- Profile Management: Teachers can manage their personal information and availability.
* Class Scheduling: Teachers can schedule classes via Google Meet integration, allowing for easy and efficient online lessons.
+ Inbox: Teachers can communicate with students who have contacted them.

### Student Functionality
- Browse Teachers: Students can browse through the list of teachers, view their profiles, and contact them for lessons.
* Inbox: Students can message teachers and keep track of their conversations.

### Messaging System
- Two-Way Communication: A built-in inbox feature allows students to initiate conversations with teachers. Teachers can respond to these messages.
* Real-Time Chat: Messages are displayed in a chat-like interface for easy communication.

### Google Calendar Integration
- Class Scheduling: Teachers can schedule classes with students using Google Calendar integration, making it easy to set up and manage online classes via Google Meet.

## Distinctiveness and Complexity:

This project demonstrates distinctiveness through its tailored functionalities for students and teachers in a language school context. It features a custom user model (CustomUser) to differentiate roles, integrates Google Calendar for scheduling, and offers a messaging system for real-time communication. The ability for teachers to manage their availability and for students to browse and contact teachers adds a unique layer of interactivity.

In terms of complexity, the project involves managing intricate data relationships between users and profiles, handling OAuth 2.0 authentication for Google Calendar integration, and ensuring real-time message handling. The integration of Tailwind CSS and JavaScript for a responsive UI further adds to the project's technical depth, requiring careful error handling and robust debugging to ensure a seamless user experience.

## File Structure 