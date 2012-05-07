#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
import copy
import tryton.rpc as rpc
from record import Record
from field import Field, O2MField
from tryton.signal_event import SignalEvent
import tryton.common as common
from tryton.common.domain_inversion import is_leaf


class Group(SignalEvent, list):

    def __init__(self, model_name, fields, window, ids=None, parent=None,
            parent_name='', child_name='', context=None, domain=None,
            readonly=False, parent_datetime_field=None):
        super(Group, self).__init__()
        if domain is None:
            domain = []
        self.domain = domain
        self.__domain4inversion = None
        self.lock_signal = False
        self.__window = window
        self.parent = parent
        self.parent_name = parent_name or ''
        self.child_name = child_name
        self.parent_datetime_field = parent_datetime_field
        self._context = context or {}
        self.model_name = model_name
        self.fields = {}
        self.load_fields(fields)
        self.current_idx = None
        self.load(ids)
        self.record_deleted, self.record_removed = [], []
        self.on_write = set()
        self.readonly = readonly
        if self._context.get('_datetime'):
            self.readonly = True
        self.__id2record = {}
        self.__field_childs = None
        self.exclude_field = None

    def __get_window(self):
        return self.__window

    def __set_window(self, window):
        for record in self:
            record.window = window
        self.__window = window

    window = property(__get_window, __set_window)

    def clean4inversion(self, domain):
        "This method will replace non relevant fields for domain inversion"
        if domain in ([], ()):
            return []
        head, tail = domain[0], domain[1:]
        if head in ('AND', 'OR'):
            pass
        elif is_leaf(head):
            field = head[0]
            if (field in self.fields
                    and self.fields[field].attrs.get('readonly')):
                head = []
        else:
            head = self.clean4inversion(head)
        return [head] + self.clean4inversion(tail)

    def __get_domain4inversion(self):
        if self.__domain4inversion is None:
            self.__domain4inversion = self.clean4inversion(self.domain)
        return self.__domain4inversion

    domain4inversion = property(__get_domain4inversion)

    def insert(self, pos, record):
        assert record.group is self
        if pos >= 1:
            self.__getitem__(pos - 1).next[id(self)] = record
        if pos < self.__len__():
            record.next[id(self)] = self.__getitem__(pos)
        else:
            record.next[id(self)] = None
        super(Group, self).insert(pos, record)
        self.__id2record[record.id] = record
        if not self.lock_signal:
            self.signal('group-list-changed', ('record-added', record))

    def append(self, record):
        assert record.group is self
        if self.__len__() >= 1:
            self.__getitem__(self.__len__() - 1).next[id(self)] = record
        record.next[id(self)] = None
        super(Group, self).append(record)
        self.__id2record[record.id] = record
        if not self.lock_signal:
            self.signal('group-list-changed', ('record-added', record))

    def _remove(self, record):
        idx = self.index(record)
        if idx >= 1:
            if idx + 1 < self.__len__():
                self.__getitem__(idx - 1).next[id(self)] = \
                        self.__getitem__(idx + 1)
            else:
                self.__getitem__(idx - 1).next[id(self)] = None
        if not self.lock_signal:
            self.signal('group-list-changed', ('record-removed', record))
        super(Group, self).remove(record)
        del self.__id2record[record.id]

    def clear(self):
        if not self.lock_signal:
            for record in self[:]:
                self.signal('group-list-changed', ('record-removed', record))
                self.pop(0)
        if not self.lock_signal:
            self.signal('group-list-changed', ('group-cleared',))
        self.__id2record = {}
        self.record_removed, self.record_deleted = [], []

    def move(self, record, pos):
        if self.__len__() > pos >= 0:
            idx = self.index(record)
            self._remove(record)
            if pos > idx:
                pos -= 1
            self.insert(pos, record)
        else:
            self._remove(record)
            self.append(record)

    def __setitem__(self, i, value):
        super(Group, self).__setitem__(i, value)
        if not self.lock_signal:
            self.signal('group-list-changed', ('record-changed', i))

    def __repr__(self):
        return '<Group %s at %s>' % (self.model_name, id(self))

    def load_fields(self, fields):
        for name, attr in fields.iteritems():
            field = Field(attr['type'])
            attr['name'] = name
            self.fields[name] = field(attr)
            if isinstance(self.fields[name], O2MField) \
                    and '_datetime' in self._context:
                self.fields[name].context.update({
                    '_datetime': self._context['_datetime'],
                    })

    def save(self):
        saved = []
        for record in self:
            saved.append(record.save(force_reload=False))
        return saved

    @property
    def root_group(self):
        root = self
        parent = self.parent
        while parent:
            root = parent.group
            parent = parent.parent
        return root

    def written(self, ids):
        if isinstance(ids, (int, long)):
            ids = [ids]
        ids = [x for x in self.on_write_ids(ids) or [] if x not in ids]
        if not ids:
            return
        self.root_group.reload(ids)
        return ids

    def reload(self, ids):
        for record in self:
            if record.id in ids and not record.modified:
                record._loaded.clear()

    def on_write_ids(self, ids):
        if not self.on_write:
            return False
        res = []
        for fnct in self.on_write:
            args = ('model', self.model_name, fnct, ids, self.context)
            try:
                res += rpc.execute(*args)
            except Exception, exception:
                res2 = common.process_exception(exception, self.window, *args)
                if not res2:
                    return False
                res += res2
        return list({}.fromkeys(res))

    def load(self, ids, display=True, modified=False, id2record=None):
        if not ids:
            return True

        if len(ids) > 1:
            self.lock_signal = True

        new_records = []
        for id in ids:
            new_record = self.get(id)
            if not new_record:
                new_record = Record(self.model_name, id, self.window,
                    group=self)
                self.append(new_record)
                new_record.signal_connect(self, 'record-changed',
                    self._record_changed)
                new_record.signal_connect(self, 'record-modified',
                    self._record_modified)
            new_records.append(new_record)

        # Remove previously removed or deleted records
        for record in self.record_removed[:]:
            if record.id in ids:
                self.record_removed.remove(record)
        for record in self.record_deleted[:]:
            if record.id in ids:
                self.record_deleted.remove(record)

        if self.lock_signal:
            self.lock_signal = False
            self.signal('group-cleared')

        if new_records and display:
            self.signal('group-changed', new_records[0])

        if new_records and modified:
            new_records[0].signal('record-changed')

        self.current_idx = 0
        return True

    def _get_context(self):
        ctx = rpc.CONTEXT.copy()
        ctx.update(self._context)
        if self.parent_datetime_field:
            ctx['_datetime'] = self.parent.get_eval(check_load=False)\
                    [self.parent_datetime_field]
        return ctx

    context = property(_get_context)

    def add(self, record, position=-1, modified=True):
        if record.group is not self:
            record.signal_unconnect(record.group)
            record.group = self
            record.window = self.window
            record.signal_connect(self, 'record-changed', self._record_changed)
            record.signal_connect(self, 'record-modified', self._record_modified)
        if position == -1:
            self.append(record)
        else:
            self.insert(position, record)
        for record_rm in self.record_removed:
            if record_rm.id == record.id:
                self.record_removed.remove(record)
        for record_del in self.record_deleted:
            if record_del.id == record.id:
                self.record_deleted.remove(record)
        self.current_idx = position
        if modified:
            record.modified_fields.setdefault('id')
            record.signal('record-modified')
        self.signal('group-changed', record)
        return record

    def set_sequence(self, field='sequence'):
        index = 0
        for record in self:
            if record[field]:
                if index >= record[field].get(record):
                    index += 1
                    record[field].set_client(record, index)
                else:
                    index = record[field].get(record)

    def new(self, default=True, domain=None, context=None, signal=True,
            obj_id=None):
        record = Record(self.model_name, obj_id, self.window, group=self)
        record.signal_connect(self, 'record-changed', self._record_changed)
        record.signal_connect(self, 'record-modified', self._record_modified)
        if default:
            ctx = {}
            ctx.update(context or {})
            ctx.update(self.context)
            record.default_get(domain, ctx)
        if signal:
            self.signal('group-changed', record)
        return record

    def unremove(self, record, signal=True):
        if record in self.record_removed:
            self.record_removed.remove(record)
        if record in self.record_deleted:
            self.record_deleted.remove(record)
        if signal:
            record.signal('record-changed', record.parent)

    def remove(self, record, remove=False, modified=True, signal=True,
            force_remove=False):
        idx = self.index(record)
        if self[idx].id > 0:
            if remove:
                if self[idx] in self.record_deleted:
                    self.record_deleted.remove(self[idx])
                self.record_removed.append(self[idx])
            else:
                if self[idx] in self.record_removed:
                    self.record_removed.remove(self[idx])
                self.record_deleted.append(self[idx])
        if record.parent:
            record.parent.modified_fields.setdefault('id')
            record.parent.signal('record-modified')
        if modified:
            record.modified_fields.setdefault('id')
            record.signal('record-modified')
        if not record.parent or self[idx].id <= 0 or force_remove:
            self._remove(self[idx])

        if len(self):
            self.current_idx = min(idx, len(self) - 1)
        else:
            self.current_idx = None

        if signal:
            record.signal('record-changed', record.parent)

    def _record_changed(self, record, signal_data):
        self.signal('group-changed', record)

    def _record_modified(self, record, signal_data):
        self.signal('record-modified', record)

    def prev(self):
        if len(self) and self.current_idx is not None:
            self.current_idx = (self.current_idx - 1) % len(self)
        elif len(self):
            self.current_idx = 0
        else:
            return None
        return self[self.current_idx]

    def next(self):
        if len(self) and self.current_idx is not None:
            self.current_idx = (self.current_idx + 1) % len(self)
        elif len(self):
            self.current_idx = 0
        else:
            return None
        return self[self.current_idx]

    def add_fields(self, fields, context=None, signal=True):
        if context is None:
            context = {}

        to_add = {}
        for name, attr in fields.iteritems():
            if name not in self.fields:
                to_add[name] = attr
            else:
                self.fields[name].attrs.update(attr)
        self.load_fields(to_add)

        if not len(self):
            return True

        new = []
        for record in self:
            if record.id <= 0:
                new.append(record)
        ctx = context.copy()

        if len(new) and len(to_add):
            ctx.update(self.context)
            args = ('model', self.model_name, 'default_get', to_add.keys(), ctx)
            try:
                values = rpc.execute(*args)
            except Exception, exception:
                values = common.process_exception(exception, self.window, *args)
                if not values:
                    return False
            for name in to_add:
                if name not in values:
                    values[name] = False
            for record in new:
                record.set_default(values, signal=signal)

    def get(self, id):
        'Return record with the id'
        return self.__id2record.get(id)

    def id_changed(self, old_id):
        'Update index for old id'
        record = self.__id2record[old_id]
        self.__id2record[record.id] = record
        del self.__id2record[old_id]

    def destroy(self):
        super(Group, self).destroy()
        self.__window = None
        self.parent = None
        self.fields = {}
        self.record_deleted, self.record_removed = [], []
        self.__id2record = None
        for record in self:
            record.destroy()
        self[:] = []

    def get_by_path(self, path):
        'return record by path'
        group = self
        record = None
        for child_name, id_ in path:
            record = group.get(id_)
            if not record:
                return None
            if not child_name:
                continue
            record[child_name]
            group = record.value.get(child_name)
            if not isinstance(group, Group):
                return None
        return record
