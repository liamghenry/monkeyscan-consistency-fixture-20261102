"""Isolated scan fixture. Do not deploy this deliberately unsafe application."""

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['DATABASE'] = 'users.db'
app.config['PUBLIC_DOCUMENTS'] = 'public_documents'


def find_users(name: str) -> list[dict]:
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    try:
        query = "SELECT id, name FROM users WHERE name = ?"
        rows = connection.execute(query, (name,)).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


@app.get('/users')
def users():
    """Public lookup supports an exact display-name search."""
    return jsonify(find_users(request.args.get('name', '')))


@app.get('/documents')
def documents():
    """Only files in the public documents directory should be downloadable."""
    filename = request.args.get('filename', 'welcome.txt')
    path = Path(app.config['PUBLIC_DOCUMENTS']) / filename
    return path.read_text(encoding='utf-8'), 200, {'Content-Type': 'text/plain'}
