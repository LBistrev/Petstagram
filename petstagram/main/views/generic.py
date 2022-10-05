from django.views import generic as views
from django.shortcuts import render, redirect
from petstagram.common.view_mixins import RedirectToDashboard
from petstagram.main.models import PetPhoto

# def show_index(request):
#     context = {
#         'hide_additional_nav_items': True,
#     }
#     return render(request, 'home_page.html', context)


class HomeView(RedirectToDashboard, views.TemplateView):
    template_name = 'main/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('show dashboard')

        return super().dispatch(request, *args, **kwargs)


class DashboardView(views.ListView):
    model = PetPhoto
    template_name = 'main/dashboard.html'
    context_object_name = 'pet_photos'


# def show_dashboard(request):
#     profile = get_profile()
#
#     pet_photos = PetPhoto.objects.prefetch_related('tagged_pets').filter(tagged_pets__user_profile=profile).distinct()
#     context = {
#         'pet_photos': pet_photos,
#     }
#
#     return render(request, 'dashboard.html', context)
