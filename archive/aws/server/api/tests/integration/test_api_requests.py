
def test_service_requests(client):
    url = "/requests"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1000


def test_service_requests_start(client):
    url = "/requests?start_date=2020-01-01&limit=10000"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 9989


def test_service_requests_end(client):
    url = "/requests?start_date=2020-01-01&end_date=2020-01-02&limit=10000"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 7650


def test_service_requests_type(client):
    url = "/requests?start_date=2020-01-01&end_date=2020-01-02&type_id=2"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 298


def test_service_requests_council(client):
    url = "/requests?start_date=2020-01-01&end_date=2020-01-02&council_id=28"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 39


def test_service_requests_all(client):
    url = "/requests?start_date=2020-01-01&end_date=2020-01-02&type_id=2&council_id=28"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_updated_service_requests(client):
    url = "/requests/updated?start_date=2020-01-01&end_date=2020-01-02&limit=10000"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 7650


def test_updated_service_requests_council(client):
    url = "/requests/updated?start_date=2020-01-01&end_date=2020-01-02&council_id=28"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 39


def test_service_request(client):
    url = "/requests/1"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["srnumber"] == "1-1523590121"
    assert response.json()["typeId"] == 6
    assert response.json()["typeName"] == "Illegal Dumping"
    assert response.json()["agencyId"] == 2
    assert response.json()["agencyName"] == "Sanitation Bureau"
    assert response.json()["sourceId"] == 8
    assert response.json()["sourceName"] == "Phone Call"
    assert response.json()["councilId"] == 44
    assert response.json()["councilName"] == "Lake Balboa"
    assert response.json()["createdDate"] == "2020-01-01T00:05:00"
    assert response.json()["closedDate"] == "2020-01-02T08:43:00"
    assert response.json()["address"] == "16815 W VANOWEN ST, 91406"
    assert response.json()["latitude"] == 34.19402846
    assert response.json()["longitude"] == -118.4994716


def test_open_service_request_pins(client):
    url = "/requests/pins/open"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 43


def test_open_counts_by_type(client):
    url = "/requests/counts/open/types"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 6


def test_service_request_pins(client):
    url = "/requests/pins"
    response = client.post(
        url,
        json={
            "startDate": "2020-01-01",
            "endDate": "2020-01-02",
            "councilIds": [
                40
            ],
            "typeIds": [
                4
            ]
        })
    assert response.status_code == 200
    assert len(response.json()) == 36


def test_service_request_pins_multiple(client):
    url = "/requests/pins"
    response = client.post(
        url,
        json={
            "startDate": "2020-01-01",
            "endDate": "2020-01-03",
            "councilIds": [
                1, 2, 4, 5
            ],
            "typeIds": [
                1, 2
            ]
        })
    assert response.status_code == 200
    assert len(response.json()) == 22


# def test_service_request_points(client):
#     url = "/requests/points"
#     response = client.post(
#         url,
#         json={
#             "startDate": "2020-01-01",
#             "endDate": "2020-01-02",
#             "ncList": [
#                 40
#             ],
#             "requestTypes": [
#                 4
#             ]
#         })
#     assert response.status_code == 200
#     assert len(response.json()) == 36
