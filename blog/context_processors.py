
def site_info(request):
    site_name = "Awais's Blog"
    blog_title = "Awais's Wonderful Blog"
    blog_description = "A Blog Site by Rana Awais Ahmad"

    return {
        'site_name': site_name,
        'blog_title': blog_title,
        'blog_description': blog_description,
    }