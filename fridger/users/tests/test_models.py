import pytest
from model_bakery import baker

from fridger.users.models import Friend


@pytest.mark.django_db
class TestFriendsModels:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_user = baker.make("users.User", email="test@test.test")
        self.test_user_1 = baker.make("users.User", email="1@test.test")
        self.test_user_2 = baker.make("users.User", email="2@test.test")

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

    def test_users_are_friends_1(self):
        baker.make("users.Friend", friend_1=self.test_user_1, friend_2=self.test_user_2)

        are_friends = Friend.objects.are_friends(self.test_user_1, self.test_user_2)

        assert are_friends

    def test_users_are_friends_2(self):
        baker.make("users.Friend", friend_2=self.test_user_1, friend_1=self.test_user_2)

        are_friends = Friend.objects.are_friends(self.test_user_1, self.test_user_2)

        assert are_friends

    def test_users_are_no_friends(self):
        baker.make("users.Friend", friend_1=self.test_user_1, friend_2=self.test_user)

        are_friends = Friend.objects.are_friends(self.test_user_1, self.test_user_2)

        assert not are_friends

    def test_user_is_in_friendship(self):
        friend = baker.make("users.Friend", friend_1=self.test_user_1, friend_2=self.test_user_2)

        is_in_friendship = friend.is_in_friendship(self.test_user_2)

        assert is_in_friendship

    def test_user_is_not_in_friendship(self):
        friend = baker.make("users.Friend", friend_1=self.test_user_1, friend_2=self.test_user_2)

        is_in_friendship = friend.is_in_friendship(self.test_user)

        assert not is_in_friendship
