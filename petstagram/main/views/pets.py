from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

# def pet_action(request, form_class, success_url, instance, template_name):
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
#         'pet': instance,
#     }
#     return render(request, template_name, context)
from petstagram.main.forms import CreatePetForm, EditPetForm, DeletePetForm


class CreatePetView(views.CreateView):
    template_name = 'main/pet_create.html'
    form_class = CreatePetForm
    success_url = reverse_lazy('show dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# def create_pet(request):
#     return pet_action(request, CreatePetForm, 'show profile', Pet(user_profile=get_profile()), 'pet_create.html')


class EditPetView(views.UpdateView):
    template_name = 'main/pet_edit.html'
    form_class = EditPetForm


# def edit_pet(request, pk):
#     return pet_action(request, EditPetForm, 'show profile', Pet.objects.get(pk=pk), 'pet_edit.html')


class DeletePetView(views.DeleteView):
    template_name = 'main/pet_delete.html'
    form_class = DeletePetForm


# def delete_pet(request, pk):
#     return pet_action(request, DeletePetForm, 'show profile', Pet.objects.get(pk=pk), 'pet_delete.html')
