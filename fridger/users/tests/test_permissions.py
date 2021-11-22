import pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestFriendsPermissions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_not_friend = baker.make("users.User")
        self.test_friend = baker.make("users.User")
        self.test_friend_2 = baker.make("users.User")

        self.friendship = baker.make("users.Friend", friend_1=self.test_friend, friend_2=self.test_friend_2)

    def test_not_friend_has_no_access(self):
        friendship_id = self.friendship.id
        url = reverse("friend-accept", args=[friendship_id])
        client = APIClient()
        client.force_authenticate(self.test_not_friend)

        response = client.post(url)

        assert response.status_code == 404

    def test_friend_request_sender_has_no_access(self):
        friendship_id = self.friendship.id
        url = reverse("friend-accept", args=[friendship_id])
        client = APIClient()
        client.force_authenticate(self.test_friend)

        response = client.post(url)

        assert response.status_code == 403

    def test_friend_request_receiver_has_access(self):
        friendship_id = self.friendship.id
        url = reverse("friend-accept", args=[friendship_id])
        client = APIClient()
        client.force_authenticate(self.test_friend_2)

        response = client.post(url)

        assert response.status_code == 200
