
class ApiRouter(object):
    hamster_models = ['Activities', 'Categories', 'FactTags', 'Facts', 'Tags']

    hamster_db = 'hamster'

    def db_for_read(self, model, **hints):
        if model.__name__ in self.hamster_models:
            return self.hamster_db
        return None

    def db_for_write(self, model, **hints):
        return False

    def allow_relation(self, obj1, obj2, **hints):
        if obj1.__class__.__name__ in self.hamster_models \
                and obj2.__class__.__name__ in self.hamster_models:
            return True
        return None

    def allow_syncdb(self, db, model):
        return False
