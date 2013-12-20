from models import Category

def decode_url(url):
    name = url.replace('_', ' ')
    return name

def get_category_list():
    cat_list = Category.objects.order_by('-name')
    for category in cat_list:
        category.url = category.name.replace(' ', '_')
    return cat_list