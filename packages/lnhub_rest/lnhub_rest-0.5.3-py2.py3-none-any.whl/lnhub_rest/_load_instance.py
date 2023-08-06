from typing import Tuple, Union

from lnhub_rest import check_breaks_lndb_and_error
from lnhub_rest._sbclient import connect_hub_with_auth
from lnhub_rest.schema import Instance, Storage


def load_instance(
    *,
    owner: str,  # owner handle
    name: str,  # instance name
) -> Union[Tuple[Instance, Storage], str]:
    hub = connect_hub_with_auth()
    try:
        check_breaks_lndb_and_error(hub)  # assumes that only called from within lndb
        # get account
        data = hub.table("account").select("*").eq("handle", owner).execute().data
        account = data[0]

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
        instance = Instance(**data[0])

        # get default storage
        data = (
            hub.table("storage")
            .select("*")
            .eq("id", instance.storage_id)
            .execute()
            .data
        )
        if len(data) == 0:
            return "storage-does-not-exist-on-hub"
        storage = Storage(**data[0])

        return instance, storage
    except Exception:
        return "loading-instance-failed"
    finally:
        hub.auth.sign_out()
