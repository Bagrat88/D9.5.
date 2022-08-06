from django import template
from News_Portal.models import Post, Tag


register = template.Library()


@register.inclusion_tag('News_Portal/popular_posts_tpl.html')
def get_popular(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt]
    return {"posts": posts}


@register.inclusion_tag('News_Portal/tags_tpl.html')
def get_tags():
    tags = Tag.objects.all
    return {"tags": tags}
