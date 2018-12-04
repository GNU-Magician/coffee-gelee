from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Category, Tag
import os
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User
from . import forms

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'archive/index.html'
    model = Post
    context_object_name = 'posts'


    def get(self, request, *args, **kwargs):
        oldest = request.GET.get('old', None)
        req = request.GET.get('err', None)


        if oldest == '1':
            list_view_sum = [x for x in Post.objects.all().order_by('-post_date')]
            list_view_false = [x for x in Post.objects.all().filter(can_view=True).order_by('-post_date')]

        else:
            list_view_sum = [x for x in Post.objects.all().order_by('post_date')]
            list_view_false = [x for x in Post.objects.all().filter(can_view=True).order_by('post_date')]


        if request.user.has_perm('Post.can_view_posts'):
            return render(request, template_name='archive/index.html',
                          context={'list':list_view_sum,
                                   'err':req,
                                   'categories':Category.objects.all()})

        return render(request, template_name='archive/index.html', context={'list': list_view_false,
                                                                            'err':req,
                                                                            'categories':Category.objects.all()})

    def get_queryset(self):
        return Post.objects.order_by('-post_date')[:15]



def DetailView(request, pk):
    object = get_object_or_404(Post, pk=pk)
    if not object.can_view and not request.user.has_perm('Post.can_view_posts'):
        return HttpResponseRedirect('%s?err=1' % reverse_lazy('archive:index'))

    else:
        return render(request, template_name='archive/post_detail.html', context={'post': object})


class CreatePostView(generic.CreateView):
    model = Post
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = forms.NameForm(request.POST, request.FILES)

        if form.is_valid():
            Post(name=form.cleaned_data['name'],
                 file=form.cleaned_data['file'],
                 post_date=timezone.now(),
                 category=Category.objects.get(pk=form.cleaned_data['category']),
                 description=form.cleaned_data['description'],
                 tag=None,
                 user=request.user,
                 can_view=form.cleaned_data['can_see']).save()
            return HttpResponseRedirect(reverse_lazy('archive:index'))

    def get(self, request, *args, **kwargs):

        form = forms.NameForm()
        return render(request, template_name='archive/create_post.html', context={'form': form})


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


class DeleteView(generic.DeleteView):
    template_name = 'archive/confirm_delete.html'
    success_url = reverse_lazy('archive:index')
    model = Post
    def get(self, request, pk, *args, **kwargs):
        if request.user != Post.objects.get(pk=pk).user:
            return HttpResponseRedirect('%s?err=1' % reverse_lazy('archive:index'))
        else:
            return render(request, 'archive/confirm_delete.html')



def CategoryList(request, pk):
    obj = Post.objects.filter(category_id=pk)
    categories = Category.objects.all()
    category = Category.objects.get(pk=pk)
    return render(request, template_name='archive/category.html', context={'posts': obj, 'categories':categories, 'category':category})

def category_create_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('descript')
        Category(name=name, description=description).save()
        return HttpResponseRedirect(reverse_lazy('archive:index'))

    else:
        return render(request, template_name='archive/create_category.html')


class UpdatePostView(generic.UpdateView):
    model = Post
    success_url = reverse_lazy('archive:index')
    template_name = 'archive/update_post.html'

    def get(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(Post, pk=pk)
        form = forms.UpdateForm()
        context = {
            'post': obj,
            'form':form,
            }
        return render(request, template_name='archive/create_post.html', context=context)

    def post(self, request, pk, *args, **kwargs):
        form = forms.UpdateForm(request.POST, request.FILES)
        if form.is_valid:

            category = Category.objects.get(pk=form.cleaned_data['category'])

            inst = Post(pk=pk,
                       name=form.cleaned_data['name'],
                       file=form.cleaned_data['file'],
                       user=request.user,
                       description=form.cleaned_data['description'],
                       category=category,
                       can_view=form.cleaned_data['can-see'],
                       tag=None)
            inst.save()

            return HttpResponseRedirect(reverse_lazy('archive:index'))


def register(request):
    all_users = User.objects.all()


    if request.method == 'GET':
        form = forms.RegisterForm()
        return render(request, template_name='archive/register.html', context={'form':form})

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return HttpResponseRedirect('/')






