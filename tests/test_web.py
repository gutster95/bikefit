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
    assert client.delete(f"/api/sitzungen/{s['id']}").status_code == 200
    assert client.get(f"/api/sitzungen/{s['id']}").status_code == 404
    assert client.delete("/api/sitzungen/..").status_code in (404, 405)


def test_model_presets_are_plausible():
    from bikefit.web.geometry import presets
    models = presets()
    assert len({(m["marke"], m["modell"]) for m in models}) >= 20
    assert any(m["modell"] == "Endurace CF SLX" and m["jahre"] == "2024–2025" for m in models)
    for m in models:
        stacks = [g["stack_mm"] for g in m["groessen"]]
        assert stacks == sorted(stacks), m["modell"]
        for g in m["groessen"]:
            assert 480 <= g["stack_mm"] <= 670 and 340 <= g["reach_mm"] <= 440, (m["modell"], g)
            assert g["sitzwinkel_grad"] is None or 72 <= g["sitzwinkel_grad"] <= 76
            assert g["kurbel_mm"] in (None, 165, 170, 172.5, 175)
