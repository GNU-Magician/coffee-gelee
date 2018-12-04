from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from coffeé_geleé.decorators import user_is_writer
app_name = 'archive'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('post/<int:pk>', views.DetailView, name='post_detail'),

    path('post/detail/<str:path>', views.download, name='download'),

    path('post/create', permission_required('Post.can_view_posts')(views.CreatePostView.as_view()), name='create_post'),

    path('post/<int:pk>/delete', user_is_writer(views.DeleteView.as_view()), name='delete'),

    path('category/posts/<int:pk>', views.CategoryList, name='category'),

    path('category/create', views.category_create_page, name='create_category'),

    path('post/<int:pk>/update', user_is_writer(views.UpdatePostView.as_view()), name='update_post'),

    path('register/', views.register, name='register_user'),


]