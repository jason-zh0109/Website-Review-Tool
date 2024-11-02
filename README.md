# website-review-tool

### Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Local Setup Instructions](#local-setup-instructions)
   - [Clone the Repository](#1-clone-the-repository)
   - [Install Python Dependencies](#2-install-python-dependencies)
   - [Apply Migrations and Create Superuser](#3-apply-migrations-and-create-superuser)
   - [Collect Static Files](#4-collect-static-files)
   - [Run the Django Backend](#5-run-the-django-backend)
   - [Access the Application](#6-access-the-application)
5. [Troubleshooting](#troubleshooting)
6. [License](#license)

## Overview
A tool that can review a defined range of UoM websites (internal and external), and detect thing like broken links and specified text or other user defined content, and return results which highlight hits and link to impacted pages to facilitate repair and update (currently, we need to eyeball webpages and click hundreds of links to check this – given structure of UoM websites this makes keeping webisted up to date virtually impossible). As an extension, if the tool could do the same for documents stored in a SharePoint site, that would be super ace.

## Features
- Review public and UniMelb restricted (In Progress) websites for broken links and specific keywords
- Admin-controlled user registration and access
- Custom keyword and content detection
- Wildcard search for specific text or keywords.

## Technologies Used

- **Django** - Backend framework
- **AWS Elastic Beanstalk** - Deployment platform
- **AWS RDS (MySQL)** - Relational database service
- **HTML/CSS/JavaScript** - Frontend development
- **AWS CodePipeline** - CI/CD

## Setup Instructions

### 1. Access the Web Application
To use the web application, simply click on the provided link: [Website Review Tool](http://env1.eba-wy6fcmup.ap-southeast-2.elasticbeanstalk.com/). No local setup is required to use this tool as this is a hosted web app, but you can find the local setup instructions at the bottom. 

### 2. User Registration and Login
- Register as a user to access public websites.
- UoM-specific and restricted content will require you to have a valid UoM account.

## Repository Structure

```
├── .ebextensions/
├── .github/workflows/
├── .idea/
├── .platform/nginx/conf.d/
├── apps/
│   ├── login/               # Handles user authentication, login, and logout
│   └── search_link/         # Handles search functionality and link review
├── resources/ui_component/   # UI components for the frontend
├── static/
├── staticfiles/admin/
├── templates/                # HTML templates for rendering web pages
├── website_review_tool/       # Main project folder
│   └── __init__.py
├── .gitattributes
├── .gitignore
├── Pipfile
├── README.md
├── manage.py                 # Django project management file
└── requirements.txt          # Python dependencies for the project
```


## Local Setup Instructions

### 1. Clone the Repository

First, clone the repository and navigate into the project directory:
```bash
git clone <https://github.com/zhonghao-sheng/website_review_tool.git>
cd website_review_tool
```
### 2. Install Python Dependencies

Ensure you have Python 3.x installed. Use pip to install the necessary Python dependencies:
```bash
pip install -r requirements.txt
```
If you haven’t already, it’s recommended to set up a virtual environment for managing dependencies:
```bash
python -m venv venv
source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
```
Then install the dependencies inside the virtual environment:
```bash
pip install -r requirements.txt
```
### 3. Apply Migrations and Create Superuser

Before running the Django server, apply the database migrations and create a superuser for admin access.

Apply migrations to set up the database schema:
```bash
python manage.py migrate
```
Create a superuser to access the admin panel:
```bash
python manage.py createsuperuser
```
Follow the prompts to set up a username, email, and password for the admin user.

### 4. Collect Static Files

Run the following command to collect all static files (necessary for Django):
```bash
python manage.py collectstatic
```
### 5. Run the Django Backend

Start the Django development server:
```bash
python manage.py runserver
```
The Django server should be running at [<http://localhost:8000>](http://localhost:8000).

### 6. Access the Application

Open your browser and go to [<http://localhost:8000>](http://localhost:8000) to access the application.

### Troubleshooting

If you encounter issues with dependency installation, ensure that pip is up to date.

If there are errors when running the server, check the logs for any missing dependencies or misconfigurations.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
