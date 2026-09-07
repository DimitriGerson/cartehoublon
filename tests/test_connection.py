from app.db import connection


def test_execute_query(monkeypatch):
    class FakeCursor:
        def execute(self, query, params):
            assert query == "SELECT * FROM houblons"
            assert params == ()

        def fetchall(self):
            return [
                {"id": 1, "nom": "Cascade"},
                {"id": 2, "nom": "Centennial"},
            ]

    class FakeConnection:
        def __init__(self):
            self.closed = False

        def cursor(self):
            return FakeCursor()

        def close(self):
            self.closed = True

    fake_conn = FakeConnection()

    monkeypatch.setattr(connection, "get_db", lambda: fake_conn)

    result = connection.execute_query("SELECT * FROM houblons")

    assert result == [
        {"id": 1, "nom": "Cascade"},
        {"id": 2, "nom": "Centennial"},
    ]

    assert fake_conn.closed is True
