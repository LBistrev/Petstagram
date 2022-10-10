from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from petstagram.main.forms import EditPetPhotoForm
from petstagram.main.models import PetPhoto


# def pet_photo_action(request, form_class, success_url, instance, template_name):
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
#         'pet_photo': instance,
#     }
#     return render(request, template_name, context)


class PetPhotoDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = PetPhoto
    template_name = 'main/photo_details.html'
    context_object_name = 'pet_photo'
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        viewed_pet_photos = request.session.get('last_viewed_pet_photo_ids', [])
        viewed_pet_photos.insert(0, self.kwargs['pk'])
        request.session['last_viewed_pet_photo_ids'] = viewed_pet_photos[:4]
        return response

    def get_queryset(self):
        return super().get_queryset().prefetch_related('tagged_pets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        return context


# def show_pet_photo_details(request, pk):
#     pet_photo = PetPhoto.objects.prefetch_related('tagged_pets').get(pk=pk)
#     context = {
#         'pet_photo': pet_photo,
#     }
#
#     return render(request, 'photo_details.html', context)

# def create_pet_photo(request):
#     return pet_photo_action(request, CreatePetPhotoForm, 'dashboard', PetPhoto(), 'photo_create.html')


class CreatePetPhotoView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = PetPhoto
    template_name = 'main/photo_create.html'
    fields = ('photo', 'description', 'tagged_pets')
    success_url = reverse_lazy('show dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditPetPhotoView(views.UpdateView):
    model = PetPhoto
    template_name = 'main/photo_edit.html'
    fields = ('description',)
    form_class = EditPetPhotoForm

    def get_success_url(self):
        return reverse_lazy('pet photo details', kwargs={'pk': self.object.id})


# def edit_pet_photo(request, pk):
#     return pet_photo_action(request, EditPetPhotoForm, 'show profile',
#     PetPhoto.objects.get(pk=pk), 'main/photo_edit.htm')

def like_pet_photo(request, pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    pet_photo.likes += 1
    pet_photo.save()

    return redirect('pet photo details', pk)
