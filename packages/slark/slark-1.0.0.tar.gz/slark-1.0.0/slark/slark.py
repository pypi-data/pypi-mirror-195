import os.path
import orjson as json


class SlarkException(Exception):
    pass


class SlarkDB:
    db_name: str = 'db.json'
    content: dict
    _table_name: str | None = None

    def __init__(self, db_name: str | None = None, table_name: str | None = None):
        if db_name:
            self.db_name = db_name
        if not os.path.exists(self.db_name):
            open(self.db_name, 'w').close()
        if table_name:
            self._table_name = table_name

    def __str__(self):
        self.refresh()
        db = ',\n'.join(f'\t{k}: {len(v)} records' for k, v in self.content.items())
        return f'SlarkDB(\n{db}\n)'

    def write(self):
        with open(self.db_name, 'bw') as file:
            file.write(json.dumps(self.content))

    def write_table(self, rows: list):
        self.content[self._table_name] = rows
        self.write()

    def refresh(self):
        # TODO: Find Solution, so won't refresh on every single query
        with open(self.db_name, 'rb') as file:
            data = file.read()
            self.content = json.loads(data) if data else {}

    def table(self, table_name: str):
        self._table_name = table_name
        return self

    @property
    def table_name(self):
        return self._table_name

    def _create_object(self, data: dict, /):
        return SlarkObject(table_name=self.table_name, db_name=self.db_name, **data)

    def get_table(self) -> list:
        if self._table_name is None:
            raise SlarkException('You should call table() first.')

        self.refresh()
        return self.content.get(self._table_name, [])

    def create(self, **kwargs):
        rows = self.get_table()
        kwargs['_id'] = len(rows) + 1
        rows.append(kwargs)
        self.write_table(rows)
        return self._create_object(kwargs)

    def get(self, **kwargs):
        rows = self.get_table()
        for r in rows:
            for k, v in kwargs.items():
                if r.get(k) == v:
                    return self._create_object(r)

    def first(self):
        rows = self.get_table()
        return self._create_object(rows[0])

    def last(self):
        rows = self.get_table()
        return self._create_object(rows[-1])

    def filter(self, **kwargs):
        rows = self.get_table()
        if not kwargs:
            return len(rows)

        result = list()
        for r in rows:
            for k, v in kwargs.items():
                if r.get(k) != v:
                    break
            else:
                result.append(self._create_object(r))
        return result

    def all(self):
        return [self._create_object(r) for r in self.get_table()]

    def count(self, **kwargs):
        rows = self.get_table()
        if not kwargs:
            return len(rows)

        result = 0
        for r in rows:
            for k, v in kwargs.items():
                if r.get(k) != v:
                    break
            else:
                result += 1
        return result

    def delete(self):
        self._check_is_slark_obj()
        rows = self.get_table()
        for r in rows:
            if r.get('_id') == self._id:
                rows.remove(r)
                self.write_table(rows)
                break

    def delete_one(self, **kwargs) -> bool:
        rows = self.get_table()
        if not kwargs:
            return False

        index = 0
        found = False
        for r in rows:
            for k, v in kwargs.items():
                if r.get(k) != v:
                    break
            else:
                found = True
                break
            index += 1

        # Didn't find any match
        if not found:
            return False

        # Delete Matched One
        rows.pop(index)
        self.write_table(rows)
        return True

    def delete_many(self, **kwargs) -> int:
        rows = self.get_table()
        if not kwargs:
            return 0

        indexes = list()
        index = 0
        found = False
        for r in rows:
            for k, v in kwargs.items():
                if r.get(k) != v:
                    break
            else:
                indexes.append(index)
                found = True
            index += 1

        # Didn't find any match
        if not found:
            return 0

        # Delete Matched Indexes
        for i in indexes[::-1]:
            rows.pop(i)
        self.write_table(rows)
        return len(indexes)

    def update(self, **kwargs):
        self._check_is_slark_obj()
        rows = self.get_table()
        for r in rows:
            if r.get('_id') == self._id:
                for k, v in kwargs.items():
                    r[k] = v
                self.write_table(rows)

    def update_one(self, condition: dict, **kwargs) -> bool:
        rows = self.get_table()
        result = False

        if not condition:
            return result

        for r in rows:
            for k, v in condition.items():
                if r.get(k) != v:
                    break
            else:
                result = True
                for new_k, new_v in kwargs.items():
                    r[new_k] = new_v
                self.write_table(rows)

        return result

    def update_many(self, condition: dict, **kwargs) -> int:
        rows = self.get_table()
        if not condition:
            return 0

        updated_count = 0
        for r in rows:
            for k, v in condition.items():
                if r.get(k) != v:
                    break
            else:
                updated_count += 1
                for new_k, new_v in kwargs.items():
                    r[new_k] = new_v

        if updated_count:
            self.write_table(rows)
        return updated_count

    def _check_is_slark_obj(self):
        if not hasattr(self, '_id'):
            raise SlarkException('You should call this method on SlarkObject instance.')


class SlarkObject(SlarkDB):
    _id: int
    data: dict

    def __init__(self, table_name: str, db_name: str, **kwargs):
        super().__init__(db_name=db_name, table_name=table_name)
        self._id = kwargs.pop('_id')
        self.data = kwargs

    def __str__(self) -> str:
        return self.json()

    def __repr__(self) -> str:
        items = ', '.join(f'{k}={v}' for k, v in self.data.items())
        return f'{self.table_name}({items})'

    def json(self) -> str:
        return json.dumps(self.data).decode()
