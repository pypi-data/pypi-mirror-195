from riseact.client import execute_partner_query, execute_query
from riseact.topics.info.data import Organization, Partner, User


def partner_get() -> Partner:
    result = execute_partner_query(
        """
        query Partner {
            partner {
                id
                name
            }
        }
    """
    )

    return Partner(**result["partner"])


def organization_search() -> list[Organization]:
    result = execute_partner_query(
        """
        query Organizations {
            organizations {
                edges {
                    node {
                        id
                        name
                        domain
                        sitefrontUrl
                    }
                }
            }
        }
    """
    )

    return [Organization(**org["node"]) for org in result["organizations"]["edges"]]


def organization_get() -> Organization:
    result = execute_query(
        """
        query OrganizationName {
            organizations {
                id
                name
                domain
                sitefrontUrl
            }
        }
    """
    )

    return Organization(**result["organization"])


def user_get() -> User:
    result = execute_query(
        """
        query UserCurrent {
            user {
                name
                email
            }
        }
    """
    )

    return User(**result["user"])
