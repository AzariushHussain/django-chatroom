# Chatroom Django Project

This is a simple chatroom application built using Django. The project allows users to create chat rooms, send and receive messages in real-time, and see active users.

## Features
- User authentication (Sign up, Login, Logout)
- Create and manage chat rooms
- Real-time messaging using Django Channels
- List of active users in the room
- Message history for each room
- Responsive and simple UI

## Requirements
- Python 3.8+
- Django 4.0+
- Channels for real-time WebSocket support
  
## Installation
   ```bash
   # Clone this repository to your local machine:
   git clone https://github.com/AzariushHussain/django-chatroom.git

  # navigate to repository in your local machine:
   cd django-chatroom

  # Create a virtual environment
  py -m venv _name_of_virtual_environment_ (Windows)
  python -m venv _name_of_virtual_environment_ (Unix/MacOS)
  
  # Activate the virtual environment
  _name_of_virtual_environment_\Scripts\activate (Windows)
  source _name_of_virtual_environment_/bin/activate (Unix/MacOS)
  
  # Install requirements
  pip install -r requirements.txt
  
  # Create migration file
  py manage.py makemigrations
  
  # Create table in database 
  py manage.py migrate

  # Run server
  daphne chat.asgi:application      
```
