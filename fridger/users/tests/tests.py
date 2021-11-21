import pytest
from model_bakery import baker

from fridger.users.models import Friend


@pytest.mark.django_db
class TestFriends:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_user = baker.make("users.User", email="test@test.test")

    def test_user_have_no_friends(self):
        baker.make("users.Friend", _quantity=4)

        friends = Friend.objects.user_friends(self.test_user)

        assert len(friends) == 0

    def test_user_have_friends_as_friend1_or_friend2(self):
        baker.make("users.Friend", friend_1=self.test_user, _quantity=2)
        baker.make("users.Friend", friend_2=self.test_user, _quantity=2)
        baker.make("users.Friend", _quantity=2)

        all_friends_count = Friend.objects.count()
        friends = Friend.objects.user_friends(self.test_user)

        assert all_friends_count == 6
        assert len(friends) == 4
