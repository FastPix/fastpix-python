import requests
from fastpix.utilis.exceptions import APIError
from fastpix.utilis.constants import BASE_URL


def make_request(method, endpoint, headers=None, data=None, params=None):
    url = f"{BASE_URL}{endpoint}"
    headers = headers or {}

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            params=params
        )

        if response.ok:
            return response.json()
        else:
            raise APIError(
                message=f"Request failed with status {response.status_code}",
                status_code=response.status_code,
                details=response.json() if response.headers.get("content-type") == "application/json" else response.text
            )
    except requests.RequestException as e:
        raise APIError(f"Request failed: {str(e)}")
