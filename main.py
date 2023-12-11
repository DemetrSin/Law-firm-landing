from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI(debug=True)

app.mount('/static', StaticFiles(directory='static'), name='static')


templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@app.get('/services', response_class=HTMLResponse)
async def services(request: Request):
    return templates.TemplateResponse('services.html', {'request': request})


@app.get('/about', response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})

