import json
from urllib import parse
import os

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_if_university_domain(email: str):
    #For testing porpuses

    if parse.splituser(email)[1] in ["cs.ihu.gr", "gmail.com"]:
        return True

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'unies.json'), encoding="utf8") as universities:
        input_json = json.load(universities)
        for x in input_json:

            if parse.splituser(email)[1] in x["domains"]:
                return True

    return False





