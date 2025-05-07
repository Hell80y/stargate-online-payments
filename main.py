from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dummy product list
products = [
    {"id": 1, "name": "Product A", "price": 19.99},
    {"id": 2, "name": "Product B", "price": 29.99},
    {"id": 3, "name": "Product C", "price": 39.99}
]

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@app.post("/add-to-cart", response_class=RedirectResponse)
def add_to_cart(product_id: int = Form(...)):
    response = RedirectResponse(url="/cart", status_code=302)
    response.set_cookie("cart", str(product_id))
    return response

@app.get("/cart", response_class=HTMLResponse)
def cart(request: Request):
    cart_id = request.cookies.get("cart")
    selected = next((p for p in products if str(p["id"]) == cart_id), None)
    return templates.TemplateResponse("cart.html", {"request": request, "item": selected})
