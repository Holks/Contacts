from app import db


class Base(db.Model):
    __abstract__ = True

    def from_dict(self, **kwargs):
        _force = kwargs.pop("_force", False)
        readonly = self._readonly_fields if hasattr(self, "_readonly_fields") \
            else []
        # readonly fields are not added to json
        readonly += ["id", "created_at", "modified_at"]
        columns = self.__table__.columns.keys()
        print(columns)
        changes = {}
        for key in columns:
            # ignore special keys
            if key.startswith("_"):
                continue
            # if key is editable = not in readonly list
            allowed = True if _force or key not in readonly else False
            # is column key listed in kwargs
            exists = True if key in kwargs else False
            if allowed and exists:
                # get current table value for the key
                val = getattr(self, key)
                if val != kwargs[key]:
                    # no point in updating to the same value
                    changes[key] = {"old": val, "new": kwargs[key]}
                    # set column current row value
                    setattr(self, key, kwargs[key])
        return changes

    def to_dict(self):
        """
        Converts table row to json object
        """
        
        # default fields to be returned
        default = self._default_fields if hasattr(self, "_default_fields") else []
        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        # table columns
        columns = self.__table__.columns.keys()

        ret_data = {}

        # iterate all colums to apply row values to keys
        for key in columns:
            # ignore special keys
            if key.startswith("_"):
                continue
            # not to be returned
            if key in hidden:
                continue
            # only default keys are returned
            if key in default:
                ret_data[key] = getattr(self, key)
        
        # return json object
        return ret_data