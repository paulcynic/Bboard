from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Bb, Rubric
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.dates import ArchiveIndexView, DateDetailView
from django.core.paginator import Paginator
from django.forms.formsets import ORDERING_FIELD_NAME
from django.forms import inlineformset_factory
from .forms import BbForm, RegisterUserForm, RubricFormSet
from django.urls import reverse_lazy, reverse


class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


def pass_form(request):
    if request.method == 'POST':
        ps = RegisterUserForm(request.POST)
        if ps.is_valid():
            ps.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            context = {'form': ps}
            return render(request, 'bboard/passform.html', context)
    else:
        ps = RegisterUserForm()
        context = {'form': ps}
        return render(request, 'bboard/passform.html', context)


#def bbs(request, rubric_id):
#    BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
#    rubric = Rubric.objects.get(pk=rubric_id)
#    if request.method == 'POST':
#        formset = BbsFormSet(request.POST, instance=rubric)
#        if formset.is_valid():
#            formset.save()
#            return redirect('index')
#        else:
#            context = {'form': formset, 'current_rubric': rubric}
#            return render(request, 'bboard/setform.html', context)
#    else:
#        formset = BbsFormSet(instance=rubric)
#        context = {'form': formset, 'current_rubric': rubric}
#        return render(request, 'bboard/setform.html', context)



#def set_form(request):
#    if request.method == 'POST':
#        sf = RubricFormSet(request.POST)
#        if sf.is_valid():
#            for form in sf:
#                if form.cleaned_data:
#                    rubric = form.save(commit=False)
#                    rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
#                    rubric.save()
#            return HttpResponseRedirect(reverse('index'))
#        else:
#            context = {'form': sf}
#            return render(request, 'bboard/setform.html', context)
#    else:
#        sf = RubricFormSet()
#        context = {'form': sf}
#        return render(request, 'bboard/setform.html', context)

# def add_and_save(request):
#     if request.method == 'POST':
#         bbf = BbForm(request.POST)
#         if bbf.is_valid():
#             bbf.save()
#             return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
#         else:
#             context = {'form': bbf}
#             return render(request, 'bboard/create.html', context)
#     else:
#         bbf = BbForm()
#         context = {'form': bbf}
#         return render(request, 'bboard/create.html', context)


#class BbCreateView(CreateView):
#    template_name = 'bboard/create.html'
#    form_class = BbForm
#    success_url = reverse_lazy('index')
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['rubrics'] = Rubric.objects.all()
#        return context


#class BbCreateView(CreateView):
#    template_name = 'bboard/create.html'
#    form_class = BbForm
#    success_url = reverse_lazy('index')
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['rubrics'] = Rubric.objects.all()
#        return context


def index(request):
    rubrics = Rubric.objects.all()
    bbs = Bb.objects.all()
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubrics': rubrics, 'page': page, 'bbs': page.object_list}
    return render(request, 'bboard/index.html', context)


#class BbIndexView(ArchiveIndexView):
#    model = Bb
#    date_field = 'published'
#    date_list_period = 'year'
#    template_name = 'bboard/index.html'
#    context_object_name = 'bbs'
#    allow_empty = True
#
#    def get_context_data(self, *args, **kwargs):
#        context = super().get_context_data(*args, **kwargs)
#        context['rubrics'] = Rubric.objects.all()
#        return context

# def index(request):
#     # template = loader.get_template('bboard/index.html')
#     bbs = Bb.objects.all()
#     rubrics = Rubric.objects.all()
#     context = {'bbs': bbs, 'rubrics': rubrics}
#     # context = {'bbs': bbs}
#     # return HttpResponse(template.render(context, request))
#     return render(request, 'bboard/index.html', context)

#class BbByRubricView(TemplateView):
#    template_name = 'bboard/by_rubric.html'
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
#        context['rubrics'] = Rubric.objects.all()
#        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
#        return context

class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context

# def by_rubric(request, rubric_id):
#     bbs = Bb.objects.filter(rubric=rubric_id)
#     rubrics = Rubric.objects.all()
#     current_rubric = Rubric.objects.get(pk=rubric_id)
#     context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
#     return render(request, 'bboard/by_rubric.html', context)

# class BbDetailView(DateDetailView):
#     model = Bb
#     date_field = 'published'
#     month_format = '%m'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

def edit(request, pk):
    bb = Bb.objects.get(pk=pk)
    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            if bbf.has_changed():
                bbf.save()
            return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/create.html', context)
    else:
        bbf = BbForm(instance=bb)
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)

#class BbEditView(UpdateView):
#    model = Bb
#    form_class = BbForm
#    success_url = '/'
#
#    def get_context_data(self, *args, **kwargs):
#        context = super().get_context_data(*args, **kwargs)
#        context['rubrics'] = Rubric.objects.all()
#        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbRedirectView(RedirectView):
    # url = '/detail/%(pk)d/'
    pattern_name = 'detail'
