from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import logout as do_logout


@login_required
def index(request):

    return render(request, 'index.html',)


class Index(LoginRequiredMixin, TemplateView):
    template_name = "blank.html"

    def get_context_data(self, *args, **kwargs):
       pass

    def get(self, request, *args, **kwargs):
        context = {
            'action': "true",
        }

        return render(request, 'dashboard/dashboard.html', context)


def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "blank.html"

    def get_context_data(self, *args, **kwargs):
       pass

    def get(self, request, *args, **kwargs):

        context = {
            'action': "true",
        }
        return render(request, 'dashboard/dashboard.html', context)


class RegistrationUser(LoginRequiredMixin, TemplateView):
    template_name = "blank.html"

    def get_context_data(self, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):

        context = {
            'action': "false",
        }

        return render(request, 'dashboard/dashboard.html', context)


class CreateMeeetupBeer(LoginRequiredMixin, TemplateView):
    template_name = "blank.html"

    def get_context_data(self, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):

        return render(request, 'create_meeetup_beer/create_meeetup_beer.html')


class NotificationAll(LoginRequiredMixin, TemplateView):
    template_name = "blank.html"

    def get_context_data(self, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):

        return render(request, 'notification/notification.html')
