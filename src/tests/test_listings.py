import pytest
from django.contrib.auth import get_user_model
User = get_user_model()

@pytest.mark.django_db
def test_create_listing():
    user = User.objects.create_user(username="admin", password="pass1234")
    assert user.username == "admin"
