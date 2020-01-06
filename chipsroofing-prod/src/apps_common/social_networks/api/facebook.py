from ..models import SocialConfig


def post(message, url=None):
    """
        Публикация в Facebook
    """
    config = SocialConfig.get_solo()
    if not message:
        return

    import facebook
    facebook_api = facebook.GraphAPI(config.facebook_access_token)
    attachment = {}
    if url:
        attachment['link'] = url

    facebook_api.put_wall_post(message=message, attachment=attachment)
