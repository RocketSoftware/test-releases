import requests
from requests.auth import HTTPBasicAuth
import argparse
import glob

print ("Uploading artifascts to github")

parser = argparse.ArgumentParser(description='Upload artifacts to github')
parser.add_argument('-version', 
                    dest='version',
                    default='1.2.3.4',
                    help='Version of this release')
parser.add_argument('-artefacts', 
                    dest='filespec',
                    default='',
                    help='Artefacts that are to be uploaded')
parser.add_argument('--final', 
                    dest='prerelease',
                    action='store_const',
                    const=False,
                    default=True,
                    help='Specify if release is final')

args = parser.parse_args()

version = args.version
prerelease = args.prerelease

github_organization = 'RocketSoftware'
github_repository = 'test-releases'
github_release_id = '18297749'
github_user = 'hrensink'
github_password = 'R0cket1!'
uploads_url = 'https://uploads.github.com'
api_url = 'https://api.github.com'

# retrieve our release if exists
url = api_url + '/repos/' + github_organization + '/' + github_repository + '/releases/tags/' + version
res = requests.get(url=url)
if res.status_code == 200:
    res = res.json()
    url = api_url + '/repos/' + github_organization + '/' + github_repository + '/releases/' + str(res["id"])
    res = requests.delete(url=url,
                          auth=HTTPBasicAuth(github_user, github_password))
    print ("Release " + version + " was deleted (" + str(res.status_code) + ")")

    url = api_url + '/repos/' + github_organization + '/' + github_repository + '/git/refs/tags/' + version
    res = requests.delete(url=url,
                    auth=HTTPBasicAuth(github_user, github_password))
    print ("Tag " + version + " was deleted (" + str(res.status_code) + ")")

# create our release
url = api_url + '/repos/' + github_organization + '/' + github_repository + '/releases'
res = requests.post(url=url,
                    json = { 
                        "tag_name": version,
                        "target_commitish": "master",
                        "name": version,
                        "body": "Description of the version " + version,
                        "draft": False,
                        "prerelease": prerelease
                    },
                    auth=HTTPBasicAuth(github_user, github_password))
print ("Release " + version + " was created (" + str(res.status_code) + ")")

if res.status_code == 201:
    res = res.json()
    github_release_id = res["id"]

    for filename in glob.glob(args.filespec):
        data = open(filename, 'rb').read()
        url = uploads_url + '/repos/' + github_organization + '/' + github_repository + '/releases/' + str(github_release_id) + '/assets'
        res = requests.post(url=url + '?name=' + filename,
                            data=data,
                            headers={'Content-Type': 'application/octet-stream'},
                            auth=HTTPBasicAuth(github_user, github_password))

        print ("Asset " + filename + " was uploaded (" + str(res.status_code) + ")")

