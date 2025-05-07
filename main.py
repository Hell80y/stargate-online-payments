from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

products = [
    {"id": 1, "name": "Organic Avocados", "price": 3.49},
    {"id": 2, "name": "Fresh Kale Bunch", "price": 2.25},
    {"id": 3, "name": "Free-Range Eggs (12)", "price": 4.75},
    {"id": 4, "name": "Whole Grain Bread", "price": 3.00}
]

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.post("/add-to-cart", response_class=RedirectResponse)
def add_to_cart(request: Request, product_id: int = Form(...)):
    try:
        cart_cookie = request.cookies.get("cart")
        cart = json.loads(cart_cookie) if cart_cookie else []
        if not isinstance(cart, list):
            cart = []
    except Exception as e:
        print("Cart cookie parse error:", e)
        cart = []

    cart.append(product_id)
    response = RedirectResponse(url="/cart", status_code=302)
    response.set_cookie("cart", json.dumps(cart))
    return response

@app.get("/cart", response_class=HTMLResponse)
def cart(request: Request):
    try:
        cart_cookie = request.cookies.get("cart")
        cart_ids = json.loads(cart_cookie) if cart_cookie else []
        if not isinstance(cart_ids, list):
            cart_ids = []
    except:
        cart_ids = []

    cart_items = [p for p in products if p["id"] in cart_ids]
    return templates.TemplateResponse("cart.html", {"request": request, "items": cart_items})

@app.post("/remove-from-cart", response_class=RedirectResponse)
def remove_from_cart(request: Request, product_id: int = Form(...)):
    try:
        cart_cookie = request.cookies.get("cart")
        cart = json.loads(cart_cookie) if cart_cookie else []
        if not isinstance(cart, list):
            cart = []
    except:
        cart = []

    if product_id in cart:
        cart.remove(product_id)

    response = RedirectResponse(url="/cart", status_code=302)
    response.set_cookie("cart", json.dumps(cart))
    return response
