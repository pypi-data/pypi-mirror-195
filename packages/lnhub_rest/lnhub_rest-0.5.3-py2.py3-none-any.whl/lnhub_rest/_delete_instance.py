from typing import Optional, Union

from lnhub_rest import check_breaks_lndb_and_error
from lnhub_rest._sbclient import connect_hub_with_auth


def delete_instance(
    *,
    owner: str,  # owner handle
    name: str,  # instance name
    _email: Optional[str] = None,
    _password: Optional[str] = None,
    _access_token: Optional[str] = None,
) -> Union[None, str]:
    hub = connect_hub_with_auth(
        email=_email, password=_password, access_token=_access_token
    )
    check_breaks_lndb_and_error(hub)  # assumes that only called from within lndb
    try:
        # get account
        data = hub.table("account").select("*").eq("handle", owner).execute().data
        account = data[0]

        # get instance
        data = (
            hub.table("instance")
            .select("*")
            .eq("account_id", account["id"])
            .eq("name", name)
            .execute()
            .data
        )
        if len(data) == 0:
            return "instance-not-exists"

        instance = data[0]

        (
            hub.table("account_instance")
            .delete()
            .eq("instance_id", instance["id"])
            .execute()
            .data
        )

        data = hub.table("instance").delete().eq("id", instance["id"]).execute().data

        # TODO: delete storage if no other instances use it
        return None
    finally:
        hub.auth.sign_out()
