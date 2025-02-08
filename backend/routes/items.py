from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from backend.database import get_db
from backend.db import Item

router = APIRouter(prefix="/items", tags=["items"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Item,
    summary="Create an item",
    description="Create an item with information id, name, description, price and is_available.",
)
def create_item(item: Item, session: Session = Depends(get_db)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/{item_id}", status_code=status.HTTP_200_OK, response_model=Item)
def read_item(item_id: int, session: Session = Depends(get_db)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
