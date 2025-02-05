"""
FastAPI Data Ingestion: Query Parameters, Path Parameters, and Request Body

This documentation explains how FastAPI automatically ingests data from different request components
including query parameters, path parameters, and request body.

FastAPI inspects function signatures and Pydantic models to determine the source of data
and how it should be validated and structured.
"""

from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# -----------------------------
# Path Parameters
# -----------------------------
"""
Path parameters are extracted directly from the request URL.
FastAPI determines them based on the function signature.

By default, path parameters are **required** and must match the type specified in the function.
"""


@app.get("/items/{item_id}")
async def get_item(item_id: int = Path(..., title="The ID of the item to retrieve", ge=1)):
    """Extracts `item_id` from the path and enforces it as an integer >= 1."""
    return {"item_id": item_id}


# -----------------------------
# Query Parameters
# -----------------------------
"""
Query parameters are extracted from the URL's query string.

- If a default value is provided, the parameter is **optional**.
- If no default is provided, FastAPI treats it as **required**.
- The `Query(...)` function allows for additional validation and documentation.
"""


@app.get("/search/")
async def search_items(
        q: Optional[str] = Query(None, title="Search Query", min_length=3),
        limit: int = Query(10, title="Number of items to return", ge=1, le=100)):
    """Extracts optional search query and limit from the URL's query parameters."""
    return {"query": q, "limit": limit}


# -----------------------------
# Request Body
# -----------------------------
"""
Request body data is extracted from the JSON payload of the request.
FastAPI automatically deserializes the request body into a Pydantic model.

- `Body(...)` can be used to add metadata or enforce constraints (not mandatory to use that).
- If a parameter is annotated with a Pydantic model, FastAPI expects the request body.
- Unlike query/path parameters, body parameters **must be explicitly defined**.
"""


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    available: bool = True


@app.post("/items/")
async def create_item(item: Item = Body(..., title="Item Data")):
    """Accepts a structured JSON request body and validates it using Pydantic."""
    return {"message": "Item created", "item": item}




# -----------------------------
# Combining Path, Query, and Body Parameters
# -----------------------------
"""
FastAPI allows combining path, query, and body parameters in the same route.
It automatically determines where each parameter should come from.

FastAPI can automatically determine whether a parameter comes from the path, query, or request body based on its position and type annotation, 
so explicitly using Path, Query, and Body is not required. 
However, using them provides better validation, documentation, and control, such as enforcing constraints (ge=1 for integers) or improving OpenAPI descriptions.
"""


@app.put("/items/{item_id}")
async def update_item(
        item_id: int = Path(..., title="Item ID", ge=1),
        q: Optional[str] = Query(None, title="Search modifier"),
        item: Item = Body(..., title="Updated Item Data")
):
    """Combines path, query, and body parameters."""
    return {"item_id": item_id, "query": q, "updated_item": item}


# -----------------------------
# Automatic Data Ingestion and Validation
# -----------------------------
"""
- **Path parameters** are inferred from the function signature.
- **Query parameters** are detected when no matching path parameter exists.
- **Body parameters** require explicit Pydantic model annotation.
- FastAPI validates all parameters according to type hints and constraints.
- The OpenAPI schema (Swagger UI) is generated automatically based on parameter definitions.

**Example Request:**
POST /items/
{
    "name": "Laptop",
    "description": "A high-performance laptop",
    "price": 1200.50,
    "available": true
}

**Example Response:**
{
    "message": "Item created",
    "item": {
        "name": "Laptop",
        "description": "A high-performance laptop",
        "price": 1200.50,
        "available": true
    }
} 
"""
