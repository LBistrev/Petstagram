from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from petstagram.accounts.models import Profile
from petstagram.main.models import Pet

UserModel = get_user_model()


class ProfileDetailsViewTests(django_test.TestCase):
    VALID_USER_CREDENCIALS = {
        'username': 'test_user',
        'password': 'test_password',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'user_first_name',
        'last_name': 'user_last_name',
        'picture': 'http://test.picture/url.png',
        'date_of_birth': date(2000, 5, 15),
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENCIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def test_when_opening_not_existing_profile_expect_404(self):
        response = self.client.get(reverse('show profile', kwargs={
            'pk': 1,
        }))

        self.assertEqual(404, response.status_code)

    def test_expect_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()

        self.client.get(reverse('show profile', kwargs={
            'pk': profile.pk,
        }))
        self.assertTemplateUsed('accounts/profile_details.html')

    def test_when_user_is_owner__expect_is_owner_to_be_true(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENCIALS)
        response = self.client.get(reverse('show profile', kwargs={'pk': profile.pk}))

        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self):
        _, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser',
            'password': 'test_password2',
        }

        self.__create_user(**credentials)

        self.client.login(**credentials)

        response = self.client.get(reverse('show profile', kwargs={'pk': profile.pk}))

        self.assertFalse(response.context['is_owner'])

    def test_when_no_photo_likes__expect_total_likes_count_to_be_0(self):
        _, profile = self.__create_valid_user_and_profile()
        pet = Pet.objects.create()

    def test_when_there_are_no_photos__no_photos_count(self):
        pass

    def test_when_pets__should_return_owners_pets(self):
        pass

    def test_when_no_pets__pet_should_be_empty(self):
        pass

    def test_when_no_pets__likes_and_photos_count_should_be_0(self):
        pass
