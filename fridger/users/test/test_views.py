from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict
from django.urls import reverse
from model_bakery import baker, random_gen
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TestUserListTestCase(APITestCase):
    """
    Tests /users list operations.
    """

    def setUp(self):
        self.url = reverse("user-list")
        self.user_data = model_to_dict(baker.prepare(User))

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(
            self.url, {"username": self.user_data["username"], "password": self.user_data["password"]}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(pk=response.data.get("id"))
        self.assertEqual(user.username, self.user_data.get("username"))
        self.assertTrue(check_password(self.user_data.get("password"), user.password))


class TestUserDetailTestCase(APITestCase):
    """
    Tests /users detail operations.
    """

    def setUp(self):
        self.user = baker.make(User)
        self.url = reverse("user-detail", kwargs={"pk": self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_request_updates_a_user(self):
        new_first_name = random_gen.gen_string(10)
        payload = {"first_name": new_first_name}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.id)
        self.assertEqual(user.first_name, new_first_name)
