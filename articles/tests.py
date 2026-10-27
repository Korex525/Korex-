import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from articles.models import Article

User = get_user_model()

@pytest.mark.django_db
class TestArticleAPI:
    
    # 1. Test listing articles (anonymous GET)
    def test_list_articles_anonymous(self):
        client = APIClient()
        url = reverse('article-list')
        response = client.get(url)
        assert response.status_code == 200

    # 2. Test model creation
    def test_create_article_model(self):
        article = Article.objects.create(
            title="Test Article Title",
            source_url="https://example.com/test",
            content="Test content..."
        )
        assert Article.objects.count() == 1
        assert str(article) == "Test Article Title"

    # 3. Test JWT Token Endpoint
    def test_jwt_token_obtain(self):
        User.objects.create_user(username="testuser", password="testpassword123")
        client = APIClient()
        url = reverse('token_obtain_pair')
        response = client.post(url, {"username": "testuser", "password": "testpassword123"}, format="json")
        
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    # 4. Test authenticated POST request via JWT
    def test_create_article_authenticated(self):
        user = User.objects.create_user(username="testuser", password="testpassword123")
        client = APIClient()
        
        # Obtain JWT Access Token
        token_url = reverse('token_obtain_pair')
        token_response = client.post(token_url, {"username": "testuser", "password": "testpassword123"}, format="json")
        access_token = token_response.data["access"]
        
        # Set Authorization header
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        
        # Create article as authenticated user
        articles_url = reverse('article-list')
        data = {
            "title": "Auth Created Article",
            "source_url": "https://example.com/auth-created",
            "content": "Content written by authenticated user."
        }
        response = client.post(articles_url, data, format="json")
        assert response.status_code == 201
        assert response.data["title"] == "Auth Created Article"