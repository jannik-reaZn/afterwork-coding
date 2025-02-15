from fastapi import APIRouter, HTTPException, status

from backend.database import SessionDep
from backend.db import Item

router = APIRouter(prefix="/items", tags=["items"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Item,
    summary="Create an item",
    description="Create an item with information id, name, description, price and is_available.",
)
def create_item(item: Item, session: SessionDep):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/{item_id}", status_code=status.HTTP_200_OK, response_model=Item)
def read_item(item_id: int, session: SessionDep):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
