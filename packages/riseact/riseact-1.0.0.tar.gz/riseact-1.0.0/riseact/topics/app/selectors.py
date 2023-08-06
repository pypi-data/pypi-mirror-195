from dotenv import dotenv_values

from riseact.client import execute_partner_query
from riseact.topics.app.data import Application


def app_get_config() -> dict:
    return dotenv_values(".env")


def app_get_by_client_id(*, client_id: str) -> Application | None:
    result = execute_partner_query(
        """
        query AppByClientId($clientId: String!) {
            appByClientId(clientId: $clientId) {
                id
                name
                type
                organization
                appUrl
                installUrl
                authorName
                authorHomepageUrl
                redirectUris
                clientId
                clientSecret
            }
        }
    """,
        variable_values={"clientId": client_id},
    )

    found_app = result["appByClientId"]

    if found_app:
        return Application(**found_app)


def app_get(*, id: int) -> Application | None:
    result = execute_partner_query(
        """
        query AppById($id: Int!) {
            app(id: $id) {
                id
                name
                type
                organization
                appUrl
                installUrl
                authorName
                authorHomepageUrl
                redirectUris
                clientId
                clientSecret
            }
        }
    """,
        variable_values={"id": id},
    )

    found_app = result["app"]

    if found_app:
        return Application(**found_app)


def app_search() -> list[Application]:
    result = execute_partner_query(
        """
        query Apps {
            apps {
                edges {
                    node {
                        id
                        name
                        type
                        organization
                        appUrl
                        installUrl
                        authorName
                        authorHomepageUrl
                        redirectUris
                        clientId
                        clientSecret
                    }
                }
            }
        }
    """
    )

    return [Application(**app["node"]) for app in result["apps"]["edges"]]
