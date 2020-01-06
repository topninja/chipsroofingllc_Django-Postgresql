PLACEHOLDERS = {}


def register_placeholder(name, func):
    """
        Регистрация функции в качестве обработчика заглушки с именем name.
    """
    PLACEHOLDERS[name] = func
