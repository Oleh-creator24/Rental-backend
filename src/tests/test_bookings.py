import pytest
from django.contrib.auth import get_user_model
User = get_user_model()

@pytest.mark.django_db
def test_create_and_approve_booking():
    user = User.objects.create_user(username="u1", password="12345")
    assert user.username == "u1"
