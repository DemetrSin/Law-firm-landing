import uvicorn
from fastapi import FastAPI, Request, Form, BackgroundTasks, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, field_validator, PositiveInt

from send_mail import send_email_background


app = FastAPI(debug=False)

# Mount the 'static' directory for serving static files
app.mount('/static', StaticFiles(directory='static'), name='static')

# Initialize Jinja2 templates for HTML rendering
templates = Jinja2Templates(directory='templates')

# List of supported languages
supported_languages = ["en_US", "ru_RU"]


# Pydantic BaseModel for the contact form
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone: PositiveInt
    message: str

    @classmethod
    def as_form(
            cls,
            name: str = Form(),
            email: EmailStr = Form(),
            phone: str = Form(),
            message: str = Form()) -> 'ContactForm':
        """
        Convert form data to ContactForm instance.

        Args:
            name (str): Name from the form.
            email (EmailStr): Email from the form.
            phone (str): Phone number from the form.
            message (str): Message from the form.

        Returns:
            ContactForm: Instance of ContactForm.
        """
        return cls(name=name, email=email, phone=phone, message=message)

    @field_validator('name')
    @classmethod
    def name_validation(cls, value: str):
        """
        Validate the 'name' field.

        Args:
            value (str): Value of the 'name' field.

        Raises:
            HTTPException: If the value is not alpha or exceeds 100 characters.
            ValueError: If the string length exceeds 100 characters.

        Returns:
            str: Validated 'name' value.
        """
        if not value.isalpha():
            raise HTTPException(status_code=404, detail="Item not found")
        if len(value) > 100:
            raise ValueError('String length should not exceed 100 characters')
        return value

    @field_validator('message')
    @classmethod
    def message_validator(cls, value: str):
        """
        Validate the 'message' field.

        Args:
            value (str): Value of the 'message' field.

        Raises:
            ValueError: If the message length exceeds 1000 characters.

        Returns:
            str: Validated 'message' value.
        """
        if len(value) > 1000:
            raise ValueError("Message must contain no more than 1000 characters")
        return value


# class ResponseModel(BaseModel):
#     message: str
#     data: dict


# Define routes for various pages

@app.get('/', response_class=HTMLResponse)
async def get_home(request: Request):
    """
    Render the home page.

    Args:
        request (Request): FastAPI Request object.

    Returns:
        TemplateResponse: HTML template response for the home page.
    """
    return templates.TemplateResponse('home.html', {'request': request})


@app.get('/services', response_class=HTMLResponse)
async def get_services(request: Request):
    """
    Render the services page.

    Args:
        request (Request): FastAPI Request object.

    Returns:
        TemplateResponse: HTML template response for the services page.
    """
    return templates.TemplateResponse('services.html', {'request': request})


@app.get('/representatives', response_class=HTMLResponse)
async def get_representatives(request: Request):
    """
    Render the representatives page.

    Args:
        request (Request): FastAPI Request object.

    Returns:
        TemplateResponse: HTML template response for the representatives page.
    """
    return templates.TemplateResponse('representatives.html', {'request': request})


@app.get('/about', response_class=HTMLResponse)
async def get_about(request: Request):
    """
    Render the about page.

    Args:
        request (Request): FastAPI Request object.

    Returns:
        TemplateResponse: HTML template response for the about page.
    """
    return templates.TemplateResponse('about.html', {'request': request})


@app.get('/contact', response_class=HTMLResponse)
async def get_contact(request: Request):
    """
    Render the contact page.

    Args:
        request (Request): FastAPI Request object.

    Returns:
        TemplateResponse: HTML template response for the contact page.
    """
    return templates.TemplateResponse('contact.html', {'request': request})


# Handle the form submission for the contact page
@app.post("/contact")
async def post_contact(
        background_tasks: BackgroundTasks,
        request: Request,
        form: ContactForm = Depends(ContactForm.as_form)):
    """
    Handle the form submission for the contact page.

    Args:
        background_tasks (BackgroundTasks): FastAPI background tasks instance.
        request (Request): FastAPI Request object.
        form (ContactForm): Form data submitted by the user.

    Returns:
        TemplateResponse: HTML template response for the contact response page.
    """
    data = form.model_dump()
    send_email_background(background_tasks, data, request)
    return templates.TemplateResponse('contact_response.html', {'request': request, 'form': form})

# Run the FastAPI application using Uvicorn
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
