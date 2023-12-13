import uvicorn
from fastapi import FastAPI, Request, Form, BackgroundTasks, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, constr, field_validator

# import send_mail

app = FastAPI(debug=True)

app.mount('/static', StaticFiles(directory='static'), name='static')


templates = Jinja2Templates(directory='templates')


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone: str
    message: str

    @classmethod
    def as_form(cls, name: str = Form(), email: EmailStr = Form(), phone: str = Form(), message: str = Form()) -> 'ContactForm': return cls(name=name, email=email, phone=phone, message=message)


# class ResponseModel(BaseModel):
#     message: str
#     data: dict


@app.get('/', response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@app.get('/services', response_class=HTMLResponse)
async def get_services(request: Request):
    return templates.TemplateResponse('services.html', {'request': request})


@app.get('/about', response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})


@app.get('/contact', response_class=HTMLResponse)
async def get_contact(request: Request):
    return templates.TemplateResponse('contact.html', {'request': request})

#Provide SMTP
@app.post("/contact")
async def post_contact(form: ContactForm = Depends(ContactForm.as_form)):
    return form


#simple example

# @app.post('/contact')
# async def post_contact(
#     name: str = Form(...),
#     email: EmailStr = Form(...),
#     phone: str = Form(...),
#     message: str = Form(...)
# ):
#     data = {
#             "name": name,
#             "email": email,
#             "phone": phone,
#             "message": message,
#         }
#     return {"message": "Form submitted successfully!", "data": data}




#send



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