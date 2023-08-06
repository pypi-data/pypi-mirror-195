from typing import Any
from typing import Dict


__contracts__ = ["resource"]


async def present(hub, ctx) -> Dict[str, Any]:
    raise NotImplementedError


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    result = {}

    describe_ret = await hub.exec.gcp.iam.projects.service_account.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe gcp.iam.projects.service_account {describe_ret['comment']}"
        )
        return {}

    for resource in describe_ret["ret"]:
        resource_id = resource.get("resource_id")

        result[resource_id] = {
            "gcp.iam.projects.service_account.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


async def absent(hub, ctx, name: str = None, project: str = None) -> Dict[str, Any]:
    raise NotImplementedError
