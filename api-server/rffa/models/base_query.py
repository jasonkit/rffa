import sqlalchemy as sa


class BaseQuery(object):

    def __init__(self, session, Model):
        self.session = session
        self.Model = Model
        self.query = session.query(self.Model)

    def all(self):
        return self.query.all()

    def one(self):
        return self.query.one()

    def first(self):
        return self.query.first()

    def count(self):
        return self.query.count()

    def is_exist(self):
        return self.count() > 0

    def filter_by_id(self, id_):
        self.query = self.query.filter(self.Model.id == id_)
        return self

    def filter_by_page(self, page, page_size=40):
        self.query = self.query.limit(page_size)
        self.query = self.query.offset((page - 1) * page_size)
        return self

    def order_by(self, column, order='desc', cast_to=None):

        column = getattr(self.Model, column)
        if cast_to is not None:
            column = sa.cast(column, cast_to)

        if order == 'desc':
            self.query = self.query.order_by(sa.desc(column))
        elif order == 'asc':
            self.query = self.query.order_by(sa.asc(column))
        else:
            raise ValueError(
                'Wrong argument {}, expected desc or asc'.format(order))
        return self

    def filter_by_time_range(self,
                             after=None,
                             before=None,
                             column='created_at'):
        if after:
            self.query = (
                self.query
                .filter(getattr(self.Model, column) >= after)
            )

        if before:
            self.query = (
                self.query
                .filter(getattr(self.Model, column) < before)
            )

        return self
