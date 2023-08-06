from typing import Union

from xybase.reflection import get_cls_annotations, get_cls_name


class Converter:
    custom_cls_prefix: list[str]

    def __init__(self, custom_cls_prefix: Union[str, list[str]] = None):
        if custom_cls_prefix:
            self.custom_cls_prefix = custom_cls_prefix if isinstance(custom_cls_prefix, list) else [custom_cls_prefix]

    def convert(self, obj, cls):
        """ 将对象转换为其他类型 """
        if obj is None:
            return obj

        if isinstance(obj, list):
            if not obj:
                return obj

            new_items = []
            for item in obj:
                new_items.append(self.convert(item, cls))
            return new_items

        old_obj = obj if isinstance(obj, dict) else obj.__dict__
        new_obj = cls()
        annotations = get_cls_annotations(cls)

        for k in old_obj:
            v = old_obj[k]
            if v is not None and k in annotations:
                attr_cls_name = get_cls_name(annotations[k])
                if self.custom_cls_prefix and list(
                        filter(lambda b: attr_cls_name.startswith(b), self.custom_cls_prefix)):
                    setattr(new_obj, k, self.convert(v, annotations[k]))
                    continue
                setattr(new_obj, k, old_obj[k])
        return new_obj
