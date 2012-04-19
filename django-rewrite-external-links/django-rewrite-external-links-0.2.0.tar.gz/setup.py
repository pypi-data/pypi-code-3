from setuptools import setup
from rewrite_external_links import get_version
setup(
    name = "django-rewrite-external-links",
    packages = ["rewrite_external_links", ],
    include_package_data=True,
    version = get_version(),
    description = "Rewrite all external links to go via a message page.",
    author = "Incuna Ltd",
    author_email = "admin@incuna.com",
    url = "http://incuna.com/",
    install_requires = ('lxml', 'BeautifulSoup',)
)
