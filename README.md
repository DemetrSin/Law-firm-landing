# Compromise Law Firm Web Application

## Overview
This web application is built using [FastAPI](https://fastapi.tiangolo.com/) and incorporates features for a law firm, including contact forms, email notifications, and informational pages. The project follows a modular structure and utilizes various dependencies for smooth functionality.

## Project Structure
The project is organized into several files and directories:

- **main.py**: Contains the main FastAPI application with endpoints for rendering HTML pages and handling contact form submissions.
- **send_mail.py**: Defines functions for sending emails in the background using [fastapi-mail](https://github.com/sabuhish/fastapi-mail).
- **templates**: Directory containing HTML templates for different pages.
- **static**: Directory for static files such as stylesheets and images.
- **.env**: Configuration file for storing environment variables, such as email credentials.

## HTML Templates
The application uses [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) templates for rendering HTML pages. The templates include:
- **base.html**: The base template containing common elements like navigation and footer.
- **about.html, contact.html, home.html, representatives.html, services.html**: Templates for specific pages with content tailored to each section.

## Internationalization
Language support is implemented through the use of language files. JavaScript is used to dynamically update content based on the selected language. Language files are stored in the `static/languages` directory.

## Contact Form
A contact form is implemented using FastAPI's form handling capabilities. Form data is validated using Pydantic models, and emails are sent in the background with the help of `send_mail.py` and `fastapi-mail`.

## Dependencies
- **fastapi**: The main FastAPI framework for building APIs.
- **fastapi-mail**: FastAPI extension for sending emails asynchronously.
- **Jinja2**: Template engine for rendering HTML.
- **uvicorn**: ASGI server for running the FastAPI application.
- Other dependencies listed in `requirements.txt`.

## Installation
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Create a `.env` file with the required environment variables (e.g., email credentials).

## Running the Application
Execute the following command to run the application:
```bash
uvicorn main:app --reload
```
## Usage

Access the application by navigating to [http://localhost:8000](http://localhost:8000) in your web browser. Explore different sections such as services, representatives, and contact to see the functionalities in action.

## Language Localization

The application supports multiple languages. Language files are stored in the `static/languages` directory, and users can change the language dynamically using the language dropdown.
