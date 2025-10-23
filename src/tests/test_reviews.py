import pytest
from django.contrib.auth import get_user_model
User = get_user_model()

@pytest.mark.django_db
def test_add_review():
    user = User.objects.create_user(username="rev_user", password="12345")
    assert user.username == "rev_user"
