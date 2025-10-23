import pytest
from django.contrib.auth import get_user_model
User = get_user_model()

@pytest.mark.django_db
def test_jwt_token_obtain():
    user = User.objects.create_user(username="tester", password="12345")
    assert user.username == "tester"
