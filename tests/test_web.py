from fastapi.testclient import TestClient

from bikefit.web.app import create_app


def test_rider_bike_session_flow(tmp_path):
    client = TestClient(create_app(tmp_path))
    rider = client.put("/api/rider", json={"height_cm": 182, "goal": "race", "unknown": 1}).json()
    assert rider["height_cm"] == 182 and "unknown" not in rider
    bike = client.post("/api/bikes", json={"brand": "Canyon", "crank_mm": 172.5, "saddle_height_mm": 745}).json()
    assert client.get("/api/bikes").json()[0]["id"] == bike["id"]
    assert client.post("/api/sessions", json={"bike_id": "missing"}).status_code == 400
    s = client.post("/api/sessions", json={"bike_id": bike["id"]}).json()
    detail = client.get(f"/api/sessions/{s['id']}").json()
    assert detail["bike"]["brand"] == "Canyon" and detail["rounds"] == []
    assert "Canyon" in client.get("/api/brands").json()
    assert client.get("/").status_code == 200
    assert client.delete(f"/api/sessions/{s['id']}").status_code == 200
    missing = client.get(f"/api/sessions/{s['id']}?lang=de")
    assert missing.status_code == 404 and "Fitting" in missing.json()["detail"]
    assert client.delete("/api/sessions/..").status_code in (404, 405)


def test_model_presets_are_plausible():
    from bikefit.web.geometry import presets
    models = presets()
    assert len({(m["brand"], m["model"], m["years"]) for m in models}) >= 100
    assert any(m["model"] == "Endurace CF SLX" and m["years"] == "2024–2025" for m in models)
    for m in models:
        stacks = [g["stack_mm"] for g in m["sizes"]]
        assert stacks == sorted(stacks), m["model"]
        for g in m["sizes"]:
            assert 480 <= g["stack_mm"] <= 700 and 340 <= g["reach_mm"] <= 440, (m["model"], g)
            assert g["seat_angle_deg"] is None or 72 <= g["seat_angle_deg"] <= 76
            assert g["crank_mm"] in (None, 165, 170, 172.5, 175)
