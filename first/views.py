from django.shortcuts import render
from django import forms
from first.forms import TestForm, FirstForm, SecondForm
from first.models import TestModel, Author, Book
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView


def make_test_formset(request):
    # instance化する際に,initial_dataを渡すことができる(line18, 28)
    TestFormSet = forms.formset_factory(
            form=TestForm,
            extra=3,     # default-> 1
            max_num=4    # initial含めformは最大4となる
    )

    # 通常のformと同様に処理できる。
    if request.method == 'POST':
        formset = TestFormSet(request.POST)
        if formset.is_valid():
            data = repr(formset.cleaned_data)
            return HttpResponse(data)
    else:
        # formset = TestFormSet() -> 空ならこのように書く。
        formset = TestFormSet(
            initial=[
                {'title': 'No1', 'date': '2019-01-01'},
                {'title': 'No2', 'date': '2019-01-02'},
            ]
        )
    return render(request, 'first/form1.html', {'formset': formset})


def make_test_modelformset(request):
    TestModelFormSet = forms.modelformset_factory(
            model=TestModel,
            fields=('text',),
            extra=0,
            max_num=3
    )
    max_id = TestModel.objects.all()[4].pk
    if request.method == 'POST':
        #formset = TestModelFormSet(request.POST)
        formset = TestModelFormSet(request.POST,
        #     queryset=TestModel.objects.filter(text__startswith='a'), 
        queryset=TestModel.objects.filter(id__lt=max_id),
        )
        if formset.is_valid():
            formset.save()
            data = [x.text for x in TestModel.objects.all()]
            return HttpResponse(repr(data))
    else:
        # formset = TestModelFormSet(queryset=TestModel.objects.none())
        formset = TestModelFormSet(
        #        queryset=TestModel.objects.filter(text__startswith='a'),
        queryset=TestModel.objects.filter(id__lt=max_id),
        )
    return render(request, 'first/form1.html', {'formset': formset})


def make_inline_formset(request, author_id):
    author = Author.objects.get(pk=author_id)
    BookFormSet = forms.inlineformset_factory(
            parent_model=Author,
            model=Book,
            fields=('title',),
            extra=2,
    )
    if request.method == 'POST':
        formset = BookFormSet(data=request.POST, instance=author)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(author.get_absolute_url())
    else:
        formset = BookFormSet(
                instance=author,
                queryset=Book.objects.none(),
        )
    return render(request, 'first/inline_formset.html', {'formset': formset})

def make_diff_type_forms(request):
    # first_form_aとfirst_form_bは同じform(FirstForm)。
    # SecondFormはそもそも異なるFormなのでprefix不要。
    if request.method == 'POST':
        first_form_a = FirstForm(request.POST, prefix="first_a")
        first_form_b = FirstForm(request.POST, prefix="first_b")
        second_form = SecondForm(request.POST)
        if (first_form_a.is_valid()
                and first_form_b.is_valid()
                and second_form.is_valid()):
            text = 'first_a:{}<br>first_b:{}<br>second:{}'.format(
                    repr(first_form_a.cleaned_data),
                    repr(first_form_b.cleaned_data),
                    repr(second_form.cleaned_data),
            )
            return HttpResponse(text)
    else:
        first_form_a = FirstForm(prefix="first_a")
        first_form_b = FirstForm(prefix="first_b")
        second_form = SecondForm()
    return render(
            request,
            'first/diff_forms.html',
            {
                'first_a': first_form_a,
                'first_b': first_form_b,
                'second': second_form
            }
    )


def make_multiple_formsets(request):
    FirstSet = forms.formset_factory(form=FirstForm, extra=2)
    SecondSet = forms.formset_factory(form=SecondForm, extra=2)
    if request.method == 'POST':
        first_set = FirstSet(request.POST, prefix='first')
        second_set = SecondSet(request.POST, prefix='second')
        if first_set.is_valid() and second_set.is_valid():
            text = 'first:{}<br><br>second:{}'.format(
                    repr(first_set.cleaned_data),
                    repr(second_set.cleaned_data),
            )
            return HttpResponse(text)
    else:
        first_set = FirstSet(prefix='first')
        second_set = SecondSet(prefix='second')
    return render(
            request,
            'first/multiple_formsets.html',
            {
                'firstform': first_set,
                'secondform': second_set
            }
    )


class AuthorDetailView(DetailView):
    model = Author
