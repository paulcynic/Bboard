from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Bb, Rubric
from django.views.generic.edit import CreateView
from .forms import BbForm
from django.urls import reverse_lazy, reverse


def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/create.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)


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
    # template = loader.get_template('bboard/index.html')
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    # context = {'bbs': bbs}
    # return HttpResponse(template.render(context, request))
    return render(request, 'bboard/index.html', context)

def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)
