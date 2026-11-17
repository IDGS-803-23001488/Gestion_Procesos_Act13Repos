from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_inicio():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Tienda V3"}


def test_calcular_compra_correctamente():
    response = client.post(
        "/compra",
        json={"precio": 200, "descuento": 25}
    )
    assert response.status_code == 200
    assert response.json() == {
        "subtotal": 150,
        "total": 174
    }


def test_rechazar_precio_negativo():
    response = client.post(
        "/compra",
        json={"precio": -100, "descuento": 10}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Precio invalido"


def test_rechazar_descuento_negativo():
    response = client.post(
        "/compra",
        json={"precio": 100, "descuento": -10}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Descuento invalido"


def test_rechazar_descuento_mayor_a_100():
    response = client.post(
        "/compra",
        json={"precio": 100, "descuento": 110}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Descuento invalido"