from fastapi import FastAPI, HTTPException

app = FastAPI(title="FastAPI Demo", version="1.0.0")

ITEMS: dict[int, dict] = {
    1: {"id": 1, "name": "Hammer", "price": 9.99},
    2: {"id": 2, "name": "Screwdriver", "price": 4.99},
    3: {"id": 3, "name": "Wrench", "price": 7.49},
}


@app.get("/")
def health_check():
    return {"status": "healthy"}


@app.get("/items")
def list_items():
    return list(ITEMS.values())


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    return ITEMS[item_id]
