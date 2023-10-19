from django.db.models import OuterRef, Count, Subquery

from blog.models import Category, Post


def site_info(request):
    site_name = "Awais's Blog"
    blog_title = "Awais's Wonderful Blog"
    blog_description = "A Blog Site by Rana Awais Ahmad"

    return {'site_name': site_name, 'blog_title': blog_title, 'blog_description': blog_description, }


def categories_list(request):
    post_count_subquery = Post.objects.filter(category=OuterRef('pk')).filter(publish=True).annotate(
        post_count=Count('id')).values('post_count')[:1]
    categories = Category.objects.annotate(post_count=Subquery(post_count_subquery)).order_by('-post_count')[:10]
    return {'categories': categories, }
