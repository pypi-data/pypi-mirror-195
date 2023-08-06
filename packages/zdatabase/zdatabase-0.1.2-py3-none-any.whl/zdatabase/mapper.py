from zdatabase import session


class DatabaseUtils:
    @staticmethod
    def flush():
        session.flush()

    @staticmethod
    def commit():
        session.commit()

    @staticmethod
    def query(*args, **kwargs):
        return session.query(*args, **kwargs)

    @staticmethod
    def add_all(items):
        session.add_all(items)
        session.commit()
        return items


class QueryUtils:
    def select(self, params, conds):
        """ 筛选(模糊匹配）
        ?name=1&asset_sn=2019-BG-5453
        """
        flts = []
        for cond in conds:
            value = params.get(cond)
            if value:
                flts.append(getattr(self.model, cond).like(f'%{value}%'))
        return flts

    def select_(self, params, conds):
        """ 筛选(精确匹配）
        ?name=1&asset_sn=2019-BG-5453
        """
        flts = []
        for cond in conds:
            value = params.get(cond)
            if value:
                flts.append(getattr(self.model, cond) == value)
        return flts

    def select_date(self, attr_name, params):
        """ 日期筛选"""
        flts = []
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        if start_date:
            flts.append(getattr(self.model, attr_name) >= start_date)
        if end_date:
            flts.append(getattr(self.model, attr_name) <= end_date)
        return flts

    def all(self, query, method='to_json'):
        """返回全部记录
        """
        items = query.all()
        return [getattr(item, method)() for item in items]

    def paginate(self, query, params, method='to_json'):
        """分页
        page_size=100&page_num=1
        """
        page_num = params.get('page_num')
        page_size = params.get('page_size')
        page_num = int(page_num) if page_num else 1
        page_size = int(page_size) if page_size else 10
        offset_num = (page_num - 1) * page_size
        items = query.offset(offset_num).limit(page_size).all()
        total = query.count()
        rst = {
            'items': [getattr(item, method)() for item in items],
            'total': total
        }
        return rst

    def paginate2(self, query, params, method):
        """分页
        page_size=100&page_num=1
        """
        page_num = params.get('page_num')
        page_size = params.get('page_size')
        page_num = int(page_num) if page_num else 1
        page_size = int(page_size) if page_size else 10
        offset_num = (page_num - 1) * page_size
        rst = query.offset(offset_num).limit(page_size).all()
        total = query.count()
        rst = {
            'items': [method(item) for item in rst],
            'total': total
        }
        return rst


class Mapper(DatabaseUtils, QueryUtils):
    def __init__(self, model):
        self.model = model

    @staticmethod
    def jsonlize(items):
        return [item.to_json() for item in items]

    def filter(self, *args, **kwargs):
        return self.model.filter(*args, **kwargs)

    def make_flts(self, **kwargs):
        flts = []
        for k, v in kwargs.items():
            flts += [getattr(self.model, k) == v]
        return flts

    def make_query(self, **kwargs):
        flts = self.make_flts(**kwargs)
        return self.filter(*flts)

    def add_(self, data):
        obj = self.model.new(data)
        obj.add_one()
        return obj

    def add(self, data):
        obj = self.add_(data)
        self.commit()
        return obj

    def add_list_(self, items):
        for item in items:
            self.add_(item)
        self.commit()

    def save_(self, primary_key, data):
        obj = self.get_(primary_key)
        if obj:
            obj.update(data)
        else:
            self.add_(data)
        self.commit()

    def update_(self, primary_key, data):
        obj = self.get_(primary_key)
        obj.update(data)
        self.commit()

    def get_(self, primary_key):
        return self.model.query.get(primary_key)

    def get(self, primary_key):
        obj = self.get_(primary_key)
        return obj.to_json() if obj else {}

    def get_list_(self, **kwargs):
        return self.make_query(**kwargs).all()

    def get_list(self, **kwargs):
        items = self.get_list_(**kwargs)
        return self.jsonlize(items)

    def get_all_(self):
        return self.filter().all()

    def get_all(self):
        items = self.get_all_()
        return self.jsonlize(items)

    def get_attrs_(self, attr_names, **kwargs):
        flts = self.make_flts(**kwargs)
        attrs = [getattr(self.model, attr_name) for attr_name in attr_names]
        return self.query(*attrs).filter(*flts).all()

    def delete_list_(self, **kwargs):
        self.make_query(**kwargs).delete(synchronize_session=False)
        self.commit()
