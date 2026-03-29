# shoersshopapi/api/v1/address/controller.py

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.core.database import database
from .crud import AddressCrud
from shoersshopapi.api.v1.schemas import AddressSchema, AddressWithId, AddressUpdate

router = APIRouter(tags=["Addresses"])

ADDRESSNOTFOUND = HTTPException(status_code=404, detail="Address not found")

@router.post(
    "/",
    response_model=AddressWithId,
    status_code=status.HTTP_201_CREATED,
)
async def create_address(
    user_id: str,  # потом заменим на текущего пользователя из JWT
    data: AddressSchema,
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
):
    address = await AddressCrud.create_address(session, user_id, data)
    return address


@router.get(
    "/user/{user_id}",
    response_model=list[AddressWithId],
)
async def get_user_addresses(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str, # потом из JWT
):
    addresses = await AddressCrud.get_by_user(session, user_id)
    return addresses


@router.get(
    "/{address_id}",
    response_model=AddressWithId,
)
async def get_address(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    address_id: str,
):
    address = await AddressCrud.get_by_id(session, address_id)

    if not address:
        raise ADDRESSNOTFOUND 

    return address


@router.patch(
    "/{address_id}",
    response_model=AddressWithId,
)
async def update_address(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    address_id: str,
    user_id: str, # потом из JWT
    data: AddressUpdate,
):
    address = await AddressCrud.update_address(session, address_id, user_id, data)

    if not address:
        raise ADDRESSNOTFOUND 

    return address


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_address(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    address_id: str,
    user_id: str,  # потом из JWT
):
    deleted = await AddressCrud.delete_address(session, address_id, user_id)

    if not deleted:
        raise ADDRESSNOTFOUND 