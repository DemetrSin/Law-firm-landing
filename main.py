from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, constr, field_validator

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




