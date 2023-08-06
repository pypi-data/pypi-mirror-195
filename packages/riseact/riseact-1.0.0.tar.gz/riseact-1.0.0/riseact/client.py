from typing import Any, Optional

from gql import Client, gql
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport

from riseact import SETTINGS

CLIENT: Client | None = None


def client_init(partner: bool = False) -> Client:
    headers = {}
    if SETTINGS.access_token:
        headers["Authorization"] = f"Bearer {SETTINGS.access_token}"

    if partner:
        uri = f"{SETTINGS.core_host}/partners/graphql/"
    else:
        uri = f"{SETTINGS.core_host}/graphql/"

    transport = RequestsHTTPTransport(
        url=uri,
        headers=headers,
        verify=True,
        retries=3,
    )

    # Create a GraphQL client using the defined transport
    return Client(transport=transport, fetch_schema_from_transport=True)


def execute_partner_query(
    raw_query: str,
    variable_values: Optional[dict[str, Any]] = None,
):
    global CLIENT

    CLIENT = client_init(partner=True)

    try:
        return CLIENT.execute(gql(raw_query), variable_values)
    except TransportQueryError as e:
        raise e


def execute_query(
    raw_query: str,
    variable_values: Optional[dict[str, Any]] = None,
):
    global CLIENT

    CLIENT = client_init()

    try:
        return CLIENT.execute(gql(raw_query), variable_values)
    except TransportQueryError as e:
        raise e
