from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from supabase_client import supabase

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
def users(request: Request):
    try:
        result = supabase.table("users").select("*").execute()
        print("Supabase response:", result)
        return templates.TemplateResponse("users.html", {
            "request": request,
            "users": result.data
        })
    except Exception as e:
        print("ERROR:", e)
        return templates.TemplateResponse("users.html", {
            "request": request,
            "users": []
        })
