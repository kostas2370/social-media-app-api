import json
from urllib import parse
import os
from universityapp.models import University


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_if_university_domain(email: str):
    domain = parse.splituser(email)[1]

    if domain in ["cs.ihu.gr", "gmail.com"]:
        return True

    universities_check1 = University.objects.all()

    for x in universities_check1 :
        if x.email_domain == domain:
            return x.id

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'unies.json'), encoding="utf8") as universities:
        input_json = json.load(universities)
        for x in input_json:
            if domain in x["domains"]:
                return True

    return False



