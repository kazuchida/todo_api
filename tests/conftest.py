import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import Base, get_db
from app.models.todo import TodoModel


# テスト用のSQLiteデータベース（インメモリ）
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_db():
    """テスト用のデータベース接続"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # テスト用のデータベーステーブルを作成
    Base.metadata.create_all(bind=engine)
    
    # テスト用のデータベースセッションを提供
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        # テスト後にテーブルをクリア
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """テスト用のAPIクライアント"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    # データベース依存関係をオーバーライド
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    
    # テスト後に依存関係をリセット
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_todo(test_db):
    """テスト用のTODOアイテム"""
    todo = TodoModel(
        title="テスト用タスク", 
        description="これはテスト用のタスクです", 
        completed=False
    )
    test_db.add(todo)
    test_db.commit()
    test_db.refresh(todo)
    return todo