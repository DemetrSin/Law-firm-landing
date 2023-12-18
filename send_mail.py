import os
from fastapi import Request
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi.templating import Jinja2Templates
# from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env')

templates = Jinja2Templates(directory='templates')


class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME')


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
    rendered_template = templates.TemplateResponse(
        name="email.html",
        context={"request": request, "form": body},
        media_type="text/html",
    ).body

    message = MessageSchema(
        subject='Test',
        recipients=['8637868.n@gmail.com'],
        body=rendered_template,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)

    background_tasks.add_task(
        fm.send_message, message, template_name=None)
