# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import Pizza, Skladnik
from .forms import PizzaForm, SkladnikiFormSet
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.models import modelformset_factory


def index(request):
    """Strona główna"""
    kontekst = {'komunikat': 'Witaj w aplikacji Pizza!'}
    return render(request, 'pizza/index.html', kontekst)


class PizzaCreate(CreateView):
    """Widok dodawania pizzy i skladników."""

    model = Pizza
    form_class = PizzaForm
    success_url = '/pizza/lista'

    def get(self, request, *args, **kargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        skladniki = SkladnikiFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, skladniki=skladniki)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        skladniki = SkladnikiFormSet(self.request.POST)
        if form.is_valid() and skladniki.is_valid():
            return self.form_valid(form, skladniki)
        else:
            return self.form_invalid(form, skladniki)

    def form_valid(self, form, skladniki):
        pizza = form.save(commit=False)
        pizza.autor = self.request.user
        pizza.save()
        self.object = pizza
        skladniki.instance = self.object
        skladniki.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, skladniki):
        errors = skladniki.non_form_errors()
        if skladniki.total_form_count() == 0:
            skladniki = SkladnikiFormSet()
            skladniki._non_form_errors = errors
        return self.render_to_response(
            self.get_context_data(form=form, skladniki=skladniki)
        )


class PizzaUpdate(UpdateView):
    """Widok aktualizuacji"""
    model = Pizza
    form_class = PizzaForm
    context_object_name = 'pizze'
    template_name = 'pizza/pizza_form.html'
    success_url = '/pizza/lista'

    def get_context_data(self, **kwargs):
        context = super(PizzaUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['pizze'] = PizzaForm(
                self.request.POST,
                instance=self.object)
            context['skladniki'] = SkladnikiFormSet(
                self.request.POST,
                instance=self.object)
        else:
            context['pizza'] = PizzaForm(instance=self.object)
            context['skladniki'] = SkladnikiFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        skladniki = SkladnikiFormSet(self.request.POST)
        if form.is_valid() and skladniki.is_valid():
            return self.form_valid(form, skladniki)
        else:
            return self.form_invalid(form, skladniki)

    def form_valid(self, form, skladniki):
        pizza = form.save(commit=False)
        pizza.autor = self.request.user
        pizza.save()
        self.object = pizza
        skladniki.instance = self.object
        skladniki.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, skladniki):
        errors = skladniki.non_form_errors()
        if skladniki.total_form_count() == 0:
            skladniki = SkladnikiFormSet()
            skladniki._non_form_errors = errors
        return self.render_to_response(
            self.get_context_data(form=form, skladniki=skladniki)
        )

        def get_object(self, queryset=None):
            pizza = Pizza.objects.get(id=self.kwargs['pk'])
            return pizza


class PizzaDelete(DeleteView):
    model = Pizza
    template_name = 'pizza/pizza_usun.html'
    success_url = '/lista'

    def get_context_data(self, **kwargs):
        context = super(PizzaDelete, self).get_context_data(**kwargs)
        pizza = Pizza.objects.get(pk=self.object.id)
        SkladnikFormSet = modelformset_factory(
            Skladnik,
            fields=('nazwa',))
        context['skladniki'] = SkladnikFormSet(
            queryset=Skladnik.objects.filter(nazwa=pizza))
        return context
