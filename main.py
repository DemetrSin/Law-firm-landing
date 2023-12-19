from fastapi import FastAPI, Request, Form, BackgroundTasks, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, field_validator, PositiveInt
# from babel import _

from send_mail import send_email_background

app = FastAPI(debug=True)

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

supported_languages = ["en_US", "ru_RU"]


# @app.middleware("http")
# async def get_lang(request: Request, call_next):
#     lang = request.headers.get("Accept-Language", "en_US")
#     if lang not in supported_languages:
#         lang = "en_US"
#     request.state.lang = lang
#     response = await call_next(request)
#     return response


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone: PositiveInt
    message: str

    @classmethod
    def as_form(cls, name: str = Form(), email: EmailStr = Form(), phone: str = Form(), message: str = Form()) -> 'ContactForm': return cls(name=name, email=email, phone=phone, message=message)

    @field_validator('name')
    @classmethod
    def name_validation(cls, value: str):
        if not value.isalpha():
            raise HTTPException(status_code=404, detail="Item not found")
        if len(value) > 100:
            raise ValueError('String length should not exceed 100 characters')
        return value

    @field_validator('message')
    @classmethod
    def message_validator(cls, value: str):
        if len(value) > 1000:
            raise ValueError("Message must contain no more then 1000 characters")
        return value


class ResponseModel(BaseModel):
    message: str
    data: dict


@app.get('/', response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.get('/services', response_class=HTMLResponse)
async def get_services(request: Request):
    return templates.TemplateResponse('services.html', {'request': request})


@app.get('/representatives', response_class=HTMLResponse)
async def get_representatives(request: Request):
    return templates.TemplateResponse('representatives.html', {'request': request})


@app.get('/about', response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})


@app.get('/contact', response_class=HTMLResponse)
async def get_contact(request: Request):
    return templates.TemplateResponse('contact.html', {'request': request})


@app.post("/contact")
async def post_contact(background_tasks: BackgroundTasks, request: Request, form: ContactForm = Depends(ContactForm.as_form)):
    data = form.model_dump()
    send_email_background(background_tasks, data, request)
    return templates.TemplateResponse('contact_response.html', {'request': request, 'form': form})
