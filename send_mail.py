import os
from fastapi import Request
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv


# Load environment variables from a .env file
load_dotenv('.env')

# Initialize Jinja2 templates for email rendering
templates = Jinja2Templates(directory='templates')


class Envs:
    # Class to store email-related environment variables
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')


# Configuration for email connection
conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


def send_email_background(background_tasks: BackgroundTasks, body: dict, request: Request):
    """
    Send email in the background using FastAPI's BackgroundTasks.

    Args:
        background_tasks (BackgroundTasks): FastAPI background tasks instance.
        body (dict): Dictionary containing email content.
        request (Request): FastAPI Request object.

    Returns:
        None
    """
    # Render the HTML email template using Jinja2
    rendered_template = templates.TemplateResponse(
        name="email.html",
        context={"request": request, "form": body},
        media_type="text/html",
    ).body

    # Create a FastMail MessageSchema for the email
    message = MessageSchema(
        subject='Test',  # Set the email subject
        recipients=['sonofgod1551@gmail.com'],  # Set the email recipient(s)
        body=rendered_template,  # Set the HTML body of the email
        subtype=MessageType.html,  # Specify the email type as HTML
    )

    # Initialize FastMail with the provided configuration
    fm = FastMail(conf)

    # Add the task to the background tasks to send the email
    background_tasks.add_task(
        fm.send_message, message, template_name=None)
