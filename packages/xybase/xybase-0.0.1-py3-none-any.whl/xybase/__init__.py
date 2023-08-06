def singleton(cls):
    """ 单例模式 """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def group(items: list, by: str):
    """ 简单分组函数 """
    result: dict[str, list] = {}
    for item in items:
        d = item if isinstance(item, dict) else item.__dict__
        if d[by] not in result:
            result[d[by]] = []
        result[d[by]].append(item)
    return result
