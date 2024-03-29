from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import render, redirect
from django.views import generic as views

from petstagram.accounts.forms import CreateProfileForm
from petstagram.accounts.models import Profile
from petstagram.common.view_mixins import RedirectToDashboard
from petstagram.main.models import Pet, PetPhoto


# def create_profile(request):
#     return profile_action(request, CreateProfileForm, 'show index', Profile(), 'main/profile_create.html')


class UserRegisterView(RedirectToDashboard, views.CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('show dashboard')


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('show dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


# def edit_profile(request):
#     return profile_action(request, EditProfileForm, 'show profile', get_profile(), 'main/profile_edit.html')


class EditProfileView:
    pass


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'


class ProfileDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'main/../../templates/accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.object is a Profile instance
        pets = list(Pet.objects.filter(user_id=self.object.user_id))
        pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets) \
            .distinct()
        # .filter(tagged_pets__user_profile=profile)\

        total_pet_photos_count = len(pet_photos)
        total_likes_count = sum(pp.likes for pp in pet_photos)

        context.update({
            'total_likes_count': total_likes_count,
            'total_pet_photos_count': total_pet_photos_count,
            'is_owner': self.object.user_id == self.request.user.id,
            'pets': pets,
        })
        return context


# def delete_profile(request):
#     return profile_action(request, DeleteProfileForm, 'show index', get_profile(), 'main/profile_delete.html')


# def show_profile(request):
#     profile = get_profile()
#
#     pets = list(Pet.objects.filter(user_profile=profile))
#     pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets) \
#         .distinct()
#     # .filter(tagged_pets__user_profile=profile)\
#
#     total_pet_photos_count = len(pet_photos)
#     total_likes_count = sum(pp.likes for pp in pet_photos)
#
#     context = {
#         'profile': profile,
#         'total_likes_count': total_likes_count,
#         'total_pet_photos_count': total_pet_photos_count,
#         'pets': pets,
#     }
#
#     return render(request, 'profile_details.html', context)


# def profile_action(request, form_class, success_url, instance, template_name):
#     if request.method == 'POST':
#         form = form_class(request.POST, instance=instance)
#         if form.is_valid():
#             form.save()
#             return redirect(success_url)
#     else:
#         form = form_class(instance=instance)
#
#     context = {
#         'form': form,
#     }
#     return render(request, template_name, context)
