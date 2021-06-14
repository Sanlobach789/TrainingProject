from basketapp.models import Basket
from mainapp.models import SocialUrls


def basket(request):
    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    return {
        'basket': basket
    }


def social_links(request):
    links = {}
    socials = SocialUrls.objects.all()
    for item in socials:
        links[item.name] = item.url_path

    return {
        'links': links
    }
