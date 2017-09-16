from urlparse import urlparse


def get_domain(response):
    parsed_uri = urlparse(response.url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain
