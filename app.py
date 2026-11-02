"""Small Flask application used for scan testing."""

import sqlite3

from flask import Flask, jsonify, request


app = Flask(__name__)


def find_users(name: str) -> list[dict[str, str]]:
    """Return demo users matching a name supplied by an HTTP client."""
    connection = sqlite3.connect("users.db")
    connection.row_factory = sqlite3.Row
    try:
        query = "SELECT id, name FROM users WHERE name = '" + name + "'"
        rows = connection.execute(query).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


@app.get("/users")
def users():
    name = request.args.get("name", "")
    return jsonify(find_users(name))
