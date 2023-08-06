def get_cls_name(cls: type):
    """ 获取类全名(包含包名) """
    return str(cls).replace('<class \'', '').replace('\'>', '')


def get_cls_annotations(cls: type):
    """ 获取类的所有字段(包括继承父类的) """
    annotations = {}
    __get_cls_annotations__(cls, annotations)
    return annotations


def __get_cls_annotations__(cls: type, annotations: dict):
    if cls.__base__ == object:
        annotations.update(cls.__annotations__)
        return

    for base in cls.__bases__:
        __get_cls_annotations__(base, annotations)
