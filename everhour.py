import json
from requests_toolbelt.sessions import BaseUrlSession


class Resource:
    def __init__(self, api, *args, **kwargs):
        self._api = api
        self._session = api.session

    def _get(self, url):
        return self._session.get(url).json()

    def _post(self, url, data):
        return self._session.post(url, json.dumps(data)).json()

    def _delete(self, url):
        return self._session.delete(url).json()


class Users(Resource):
    def me(self):
        return self._get('/users/me')


class Team(Resource):
    def users(self):
        return self._get('/team/users')

    def timers(self):
        return self._get('/team/timers')


class Timers(Resource):
    def start(self, id_):
        return self._post('/timers', {'task': id_})

    def current(self):
        return self._get('/timers/current')

    def stop(self):
        return self._delete('/timers/current')


class Projects(Resource):
    def list(self):
        return self._get('/projects')

    def get(self, id_):
        return self._get('/projects/{0}'.format(id_))

    def tasks(self, id_):
        return self._get('/projects/{0}/tasks'.format(id_))


class Everhour:
    def __init__(self, token, *args, **kwargs):
        self.session = BaseUrlSession('https://api.everhour.com')
        self.session.headers.update({
            'X-Api-Key': token,
            'X-Accept-Version': '1.2',
            'Content-Type': 'application/json'
        })

    @property
    def users(self):
        return Users(self)

    @property
    def team(self):
        return Team(self)

    @property
    def timers(self):
        return Timers(self)

    @property
    def projects(self):
        return Projects(self)
