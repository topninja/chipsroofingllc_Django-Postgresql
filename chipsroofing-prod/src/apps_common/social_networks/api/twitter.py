from libs.description import description
from ..models import SocialConfig

POST_URL_LEN = 23
POST_START_CUT = 100
POST_MAX_LEN = 140


def format_message(message, url=None):
    """
        Форматирование сообщения для публикации в Twitter
    """
    message_len = len(message)
    if url:
        message_len += POST_URL_LEN
    if message_len >= POST_MAX_LEN:
        message = description(message, POST_START_CUT, POST_MAX_LEN - POST_URL_LEN - 1)

    if url:
        message += '\n%s' % url

    return message


def post(message, url=None):
    """
        Публикация в Twitter
    """
    config = SocialConfig.get_solo()
    message = format_message(message, url=url)
    if not message:
        return

    import twitter
    twitter_api = twitter.Api(
        config.twitter_client_id,
        config.twitter_client_secret,
        config.twitter_access_token,
        config.twitter_access_token_secret,
    )
    twitter_api.PostUpdate(message)
