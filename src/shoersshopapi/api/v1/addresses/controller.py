# shoersshopapi/api/v1/address/controller.py

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.core.database import database
from .crud import AddressCrud
from shoersshopapi.api.v1.schemas import (
    AddressSchema,
    AddressWithId,
    AddressUpdate,
    UserWithId
)

from shoersshopapi.api.v1.validators.http import (
    oauth2_scheme,
    get_current_auth_user,
    RoleRequired,
)

router = APIRouter(
    tags=["Addresses"],
    dependencies=[Depends(oauth2_scheme)]
)

ADDRESSNOTFOUND = HTTPException(status_code=404, detail="Address not found")

@router.post(
    "/",
    response_model=AddressWithId,
    status_code=status.HTTP_201_CREATED,
)
async def create_address(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    data: AddressSchema,
):
    address = await AddressCrud.create_address(session, user.id, data)
    return address


@router.get(
    "/{address_id}",
    response_model=AddressWithId,
)
async def get_address(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
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


@router.get(
    "/user/",
    response_model=list[AddressWithId],
)
async def get_self_addresses(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
):
    addresses = await AddressCrud.get_by_user(session, user.id)
    return addresses


@router.get(
    "/user/{user_id}",
    response_model=list[AddressWithId],
)
async def get_user_addresses(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,
):
    addresses = await AddressCrud.get_by_user(session, user_id)
    return addresses


@router.patch(
    "/{address_id}",
    response_model=AddressWithId,
)
async def update_address(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    address_id: str,
    data: AddressUpdate,
):
    address = await AddressCrud.update_address(session, address_id, user.id, data)

    if not address:
        raise ADDRESSNOTFOUND 

    return address


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_address(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    address_id: str,
):
    deleted = await AddressCrud.delete_address(session, address_id, user.id)

    if not deleted:
        raise ADDRESSNOTFOUND 