from models import Category

def decode_url(url):
    name = url.replace('_', ' ')
    return name

def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
    else:
        cat_list = Category.objects.all()

    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    
    for category in cat_list:
        category.url = category.name.replace(' ', '_')

    return cat_list