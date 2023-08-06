from typing import Union

from fastapi import APIRouter, Header

from .utils import (
    extract_access_token,
    get_account_permission_for_instance,
    get_supabase_client,
    supabase_client,
)

router = APIRouter(prefix="/account")


@router.get("/{id}")
def get_account_by_id(id: str):
    data = supabase_client.table("account").select("*").eq("id", id).execute().data
    return data[0] if len(data) > 0 else None


@router.get("/handle/{handle}")
def get_account_by_handle(handle: str):
    data = (
        supabase_client.table("account").select("*").eq("handle", handle).execute().data
    )
    return data[0] if len(data) > 0 else None


@router.get("/resources/owned/instances/{handle}")
def get_account_own_instances(
    handle: str, authentication: Union[str, None] = Header(default=None)
):
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)

    try:
        data = (
            supabase_client.table("account")
            .select(
                """instance!fk_instance_account_id_account(
                *, account!fk_instance_account_id_account(handle, id))""".replace(
                    "\n", ""
                )
            )
            .eq("handle", handle)
            .execute()
            .data
        )
        return data[0]["instance"] if len(data) > 0 else []

    finally:
        supabase_client.auth.sign_out()


@router.get("/resources/instances/{handle}")
def get_account_instances(
    handle: str, authentication: Union[str, None] = Header(default=None)
):
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)

    try:
        data = (
            supabase_client.table("account")
            .select(
                """account_instance(*, instance(
                *, account!fk_instance_account_id_account(handle, id)))""".replace(
                    "\n", ""
                )
            )
            .eq("handle", handle)
            .execute()
            .data
        )

        account_instances = []
        if len(data) > 0:
            for account_instance in data[0]["account_instance"]:
                if account_instance["instance"]["public"] is True:
                    account_instances.append(account_instance)
                else:
                    if authentication is not None:
                        permission = get_account_permission_for_instance(
                            account_instance["instance_id"], access_token
                        )
                        if permission is not None:
                            account_instances.append(account_instance)

        return account_instances

    finally:
        supabase_client.auth.sign_out()
