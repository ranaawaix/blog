from django.urls import path
from blog import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('add_category', views.CategoryView.as_view(), name='add-category'),
    path('update_category/<slug:slug>', views.UpdateCategory.as_view(), name='update-category'),
    path('delete_category/<slug:slug>', views.DeleteCategory.as_view(), name='delete-category'),
    path('add_post', views.CreatePost.as_view(), name='add-post'),
    path('all_posts', views.AllPosts.as_view(), name='all-posts'),
    path('category_wise_posts/<slug:slug>', views.CategoryPosts.as_view(), name='category-posts'),
    path('view_post/<slug:slug>', views.ViewPost.as_view(), name='view-post'),
    path('view_post/<slug:slug>/<int:vote>', views.VotePost.as_view(), name='vote-post'),
    path('update_post/<slug:slug>', views.UpdatePost.as_view(), name='update-post'),
    path('delete_post/<slug:slug>', views.DeletePost.as_view(), name='delete-post'),
    path('all_comments', views.AllComments.as_view(), name='all-comments'),
    path('update_comment/<int:id>', views.UpdateComment.as_view(), name='update-comment'),
    path('delete_comment/<slug:slug>', views.DeleteComment.as_view(), name='delete-comment'),
    path('create_contact', views.ContactView.as_view(), name='create-contact'),
]
