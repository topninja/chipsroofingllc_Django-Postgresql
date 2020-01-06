from libs.description import description
from ..models import SocialConfig

POST_START_CUT = 540
POST_MAX_LEN = 600


def format_message(message, url=None):
    """
        Форматирование сообщения для публикации в Twitter
    """
    message_len = len(message)
    if url:
        message_len += len(url) + 1
    if message_len >= POST_MAX_LEN:
        message = description(message, POST_START_CUT, POST_MAX_LEN)

    if url:
        message += '\n%s' % url

    return message


def post(message, url=None):
    """
        Публикация в LinkedIn
    """
    config = SocialConfig.get_solo()
    message = format_message(message, url=url)
    if not message:
        return

    from PyLinkedinAPI.PyLinkedinAPI import PyLinkedinAPI
    linkedin_api = PyLinkedinAPI(config.linkedin_access_token)
    linkedin_api.publish_profile_comment(message)
