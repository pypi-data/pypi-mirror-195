from riseact.client import execute_query
from riseact.topics.theme.data import Asset, LocalAsset, Theme, ThemeManifest


def theme_create(manifest: ThemeManifest, dev: bool) -> Theme:
    data = {
        "name": f"{manifest.name}",
        "slug": manifest.slug,
        "version": manifest.version,
        "isDevelopment": dev,
    }

    response = execute_query(
        """
        mutation ThemeCreate($data: ThemeInput!) {
            themeCreate(data: $data) {
                id
                uuid
                name
                slug
                version
                documentationUrl
                supportUrl
                isPublished
                isDevelopment
            }
        }
        """,
        variable_values={"data": data},
    )

    theme = Theme(**response["themeCreate"])

    return theme


def theme_delete(theme: Theme) -> None:
    execute_query(
        """
        mutation ThemeDelete($uuid: String!) {
            themeDelete(uuid: $uuid) {
                uuid
            }
        }
        """,
        variable_values={"uuid": theme.uuid},
    )


def asset_create(local_asset: LocalAsset, theme: Theme) -> Asset:
    data = {
        "key": local_asset.key,
        "themeId": theme.id,
        "contentType": local_asset.contentType,
        "value": local_asset.value,
        "attachment": None,
    }

    response = execute_query(
        """
        mutation AssetCreate($data: AssetInput!) {
            assetCreate(data: $data) {
                id
                key
                checksum
                contentType
                value
                attachment
                size
                updatedAt
                createdAt
            }
        }""",
        variable_values={"data": data},
    )

    asset = Asset(**response["assetCreate"])

    return asset


def asset_update(asset: Asset, local_asset: LocalAsset, theme: Theme) -> Asset:
    data = {
        "key": local_asset.key,
        "themeId": theme.id,
        "contentType": local_asset.contentType,
        "value": local_asset.value,
        "attachment": None,
    }

    response = execute_query(
        """
        mutation AssetUpdate($id: Int!, $data: AssetInput!) {
            assetUpdate(id: $id, data: $data) {
                id
                key
                checksum
                contentType
                value
                attachment
                size
                updatedAt
                createdAt
            }
        }""",
        variable_values={"id": asset.id, "data": data},
    )

    asset = Asset(**response["assetUpdate"])

    return asset


def asset_delete(asset: Asset) -> None:
    execute_query(
        """
        mutation AssetDelete($id: Int!) {
            assetDelete(id: $id) {
                id
            }
        }
        """,
        variable_values={"id": asset.id},
    )
