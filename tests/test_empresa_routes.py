


def test_crear_empresa(client):
    respuesta = client.post("/empresas/", json={
        "nombre": "Empresa de Test",
        "sitio_web": "https://test.com"
    })

    assert respuesta.status_code == 201
    assert respuesta.json()["nombre"] == "Empresa de Test"