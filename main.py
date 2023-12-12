import uvicorn
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, constr, field_validator

import send_mail

app = FastAPI(debug=True)

app.mount('/static', StaticFiles(directory='static'), name='static')


templates = Jinja2Templates(directory='templates')


class ContactForm(BaseModel):
    name: constr(min_length=1, max_length=50)
    email: EmailStr
    phone: constr()
    message: constr(min_length=20, max_length=1000)

    @field_validator("phone")
    def validate_phone(cls, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return value

    @field_validator("name")
    def validate_name(cls, value):
        if not type(value, str):
            raise ValueError("Name must be string")
        return value
@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@app.get('/services', response_class=HTMLResponse)
async def services(request: Request):
    return templates.TemplateResponse('services.html', {'request': request})


@app.get('/about', response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})


@app.get('/contact', response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse('contact.html', {'request': request})


# @app.get('/send-email/asynchronous')
# async def send_email_asynchronous():
#     await send_mail.send_email_async('Hello World','someemail@gmail.com',
#     {'title': 'Hello World', 'name': 'John Doe'})
#     return 'Success'
#
#
# @app.get('/send-email/backgroundtasks')
# def send_email_backgroundtasks(background_tasks: BackgroundTasks):
#     send_mail.send_email_background(background_tasks, 'Hello World',
#     'someemail@gmail.com', {'title': 'Hello World', 'name':       'John Doe'})
#     return 'Success'
#
#
# if __name__ == '__main__':
#     uvicorn.run('main:app', reload=True)