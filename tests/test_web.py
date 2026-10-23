from fastapi.testclient import TestClient

from bikefit.web.app import create_app


def test_rider_bike_session_flow(tmp_path):
    client = TestClient(create_app(tmp_path))
    rider = client.put("/api/fahrer", json={"groesse_cm": 182, "ziel": "rennen", "unbekannt": 1}).json()
    assert rider["groesse_cm"] == 182 and "unbekannt" not in rider
    bike = client.post("/api/raeder", json={"marke": "Canyon", "kurbel_mm": 172.5, "sattelhoehe_mm": 745}).json()
    assert client.get("/api/raeder").json()[0]["id"] == bike["id"]
    assert client.post("/api/sitzungen", json={"rad_id": "gibtsnicht"}).status_code == 400
    s = client.post("/api/sitzungen", json={"rad_id": bike["id"]}).json()
    detail = client.get(f"/api/sitzungen/{s['id']}").json()
    assert detail["rad"]["marke"] == "Canyon" and detail["runden"] == []
    assert "Canyon" in client.get("/api/marken").json()
    assert client.get("/").status_code == 200
