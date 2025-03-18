import pytest
from fastapi import status
from app.models.todo import TodoModel

# ルートエンドポイントのテスト
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Welcome to the TODO API" in response.json()["message"]


# すべてのTODOを取得するテスト
def test_get_all_todos_empty(client):
    """最初は空のTODOリストを取得するテスト"""
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_todos(client, test_todo):
    """TODOがある場合のリスト取得テスト"""
    response = client.get("/todos/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == test_todo.id
    assert response.json()[0]["title"] == test_todo.title


# 特定のTODOを取得するテスト
def test_get_todo_by_id(client, test_todo):
    """存在するTODOの取得テスト"""
    response = client.get(f"/todos/{test_todo.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_todo.id
    assert response.json()["title"] == test_todo.title


def test_get_todo_not_found(client):
    """存在しないTODOの取得テスト"""
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "Todo not found"


# 新しいTODOを作成するテスト
def test_create_todo(client):
    """新しいTODOの作成テスト"""
    todo_data = {
        "title": "新しいタスク",
        "description": "これは新しいタスクです",
        "completed": False
    }
    response = client.post("/todos/", json=todo_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["completed"] == todo_data["completed"]
    assert "id" in data


# TODOを更新するテスト
def test_update_todo(client, test_todo):
    """既存のTODOを更新するテスト"""
    updated_data = {
        "title": "更新済みタスク",
        "description": "これは更新済みのタスクです",
        "completed": True
    }
    response = client.put(f"/todos/{test_todo.id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_data["title"]
    assert data["description"] == updated_data["description"]
    assert data["completed"] == updated_data["completed"]
    assert data["id"] == test_todo.id


def test_update_todo_not_found(client):
    """存在しないTODOの更新テスト"""
    updated_data = {
        "title": "更新済みタスク",
        "description": "これは更新済みのタスクです",
        "completed": True
    }
    response = client.put("/todos/999", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# TODOを削除するテスト
def test_delete_todo(client, test_todo):
    """既存のTODOを削除するテスト"""
    response = client.delete(f"/todos/{test_todo.id}")
    assert response.status_code == 204
    
    # 削除後に再度取得を試みてNotFoundになることを確認
    response = client.get(f"/todos/{test_todo.id}")
    assert response.status_code == 404


def test_delete_todo_not_found(client):
    """存在しないTODOの削除テスト"""
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"