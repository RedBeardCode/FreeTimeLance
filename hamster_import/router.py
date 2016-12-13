from django.db.models.base import ModelBase

import hamster_import.hamster_models as hm


class ApiRouter(object):
    hamster_models =  [getattr(hm, cls_name) for cls_name in dir(hm) if isinstance(getattr(hm, cls_name), ModelBase)]
    hamster_db = 'hamster'
    def db_for_read(self, model, **hints):
        if model in self.hamster_models:
            return self.hamster_db
        return None

    def db_for_write(self, model, **hints):
        return False

    def allow_relation(self, obj1, obj2, **hints):
        if obj1 in self.hamster_models or obj2 in self.hamster_models:
            return False
        return None

    def allow_syncdb(self, db, model):
        return False