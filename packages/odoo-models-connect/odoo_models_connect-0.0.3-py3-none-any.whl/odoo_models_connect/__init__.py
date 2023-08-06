import xmlrpc.client


class ConnectOdoo(object):
    username = None
    password = None
    uid = None
    models = None

    def __init__(self, url, db):
        self.__url = url
        self.__db = db

    def authenticate(self, email, password):
        common = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(self.__url))
        uid = common.authenticate(self.__db, email, password, {})
        if uid is not False:
            self.username = email
            self.password = password
            self.uid = uid
            self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.__url))
        return uid

    def reconnect(self, obj):
        self.username = obj['username']
        self.password = obj['password']
        self.uid = obj['uid']
        self.models = obj['models']

    # def xmlrpc_odoo(self):
    #     # conectarse al servidor de Odoo
    #     url = 'http://201.219.216.217:3568'
    #     db = 'Test'
    #     username = 'constru4.0@lsv-tech.com'
    #     password = '123456'
    #     common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    #     uid = common.authenticate(self._db, self.username, self.password, {})
    #     models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    #     return {"db": db, "uid": uid, "password": password, "models": models}

    def search_read(self, model_name, condition=[], fields=[]):
        data = self.models.execute_kw(
            self.__db,
            self.uid,
            self.password,
            model_name,
            'search_read',
            [condition],
            {'fields': fields}
        )
        return data

    def read(self, model_name, object_ids, fields=[]):
        data = self.models.execute_kw(
            self.__db,
            self.uid,
            self.password,
            model_name,
            'read',
            [object_ids],
            {'fields': fields}
        )
        return data

    def search_ids(self, model_name, domain=[]):
        data = self.models.execute_kw(
            self.__db,
            self.uid,
            self.password,
            model_name,
            'search',
            [domain],
        )
        return data

    # def read(self, model_name, object_id, fields=[]):
    #     # connection = self.xmlrpc_odoo()
    #     data = self.models.execute_kw(
    #         self._db,
    #         self.uid,
    #         self.password,
    #         model_name,
    #         'read',
    #         [object_id],
    #         {'fields': fields},
    #     )
    #     return data[0]

    def create(self, model_name, data):
        self.models.execute_kw(
            self.__db,
            self.uid,
            self.password,
            model_name,
            'create',
            [data]
        )

    def write(self, model_name, object_id, data):
        self.models.execute_kw(
            self.__db,
            self.uid,
            self.password,
            model_name,
            'write',
            [[int(object_id)], data]
        )

    def delete(self, model_name, object_id):
        self.models.execute_kw(
            self.__db,
            self.uid,
            self.password,
            model_name,
            'unlink',
            [[int(object_id)]]
        )