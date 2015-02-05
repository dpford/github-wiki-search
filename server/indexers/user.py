from server.indexers import github_helpers as helpers
from server import settings
import requests
from urlparse import urljoin

def index():
    index_users(urljoin(settings.GITHUB_HOST, '/api/v3/users'))
    index_users('https://api.github.com/orgs/{}/members?per_page=9999'.format(
        settings.GITHUB_ORG))

def index_gh_users(url):
    r = requests.get(url)
    bulk_data_obj = []
    for person in r.json():
        bulk_data_obj.append({
            "index": {
                "_index": "autocomplete", 
                "_type": "user", 
                "_id": person['html_url']
        }})
        bulk_data_obj.append({
            'owner': person['login']
        })
    helpers.write_bulk_data(bulk_data_obj)