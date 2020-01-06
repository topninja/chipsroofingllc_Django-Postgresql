import requests
from social_networks.models import SocialConfig
from django.utils.functional import LazyObject, empty


class LazyYoutube(LazyObject):
    def _setup(self, name=None):
        self._wrapped = SocialConfig.get_solo()

    def request(self, resource, data):
        if self._wrapped is empty:
            self._setup()

        default = {
            'key': self._wrapped.google_apikey,
        }
        default.update(data)

        url = 'https://www.googleapis.com/youtube/v3/%s' % resource
        response = requests.get(url, params=default)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError('API response: %s' % response.status_code)


youtube = LazyYoutube()


def get_channel_info(channel_id):
    """ Информация о канале """
    result = youtube.request('channels', {
        'id': channel_id,
        'part': 'snippet,contentDetails',
        'fields': 'items(snippet/title,snippet/description,snippet/thumbnails,contentDetails/relatedPlaylists/uploads)',
    })

    try:
        item = result['items'][0]
    except (KeyError, IndexError):
        return {}

    return {
        'id': channel_id,
        'title': item['snippet']['title'],
        'description': item['snippet']['description'],
        'thumbnails': item['snippet']['thumbnails'],
        'uploads': item['contentDetails']['relatedPlaylists']['uploads'],
    }


def get_channel_playlists(channel_id, per_page=20, next_page_token=''):
    """ Список плейлистов канала """
    result = youtube.request('playlists', {
        'channelId': channel_id,
        'part': 'snippet,contentDetails',
        'fields': 'items(id,snippet/title,contentDetails/itemCount),pageInfo/*,nextPageToken',
        'pageToken': next_page_token,
        'maxResults': per_page,
    })

    return {
        'total': result['pageInfo']['totalResults'],
        'next_page_token': result.get('nextPageToken', ''),
        'items': tuple({
            'id': item['id'],
            'title': item['snippet']['title'],
            'itemCount': item['contentDetails']['itemCount'],
        } for item in result['items']),
    }


def get_playlist_videos(playlist_id, per_page=50, next_page_token=''):
    """ Список видео плейлиста """
    result = youtube.request('playlistItems', {
        'part': 'snippet',
        'playlistId': playlist_id,
        'fields': 'items('
                  'id,snippet/title,snippet/description,snippet/thumbnails,'
                  'snippet/position,snippet/resourceId),pageInfo/*,nextPageToken',
        'pageToken': next_page_token,
        'maxResults': per_page,
    })

    return {
        'total': result['pageInfo']['totalResults'],
        'next_page_token': result.get('nextPageToken', ''),
        'items': tuple({
            'id': item['snippet']['resourceId']['videoId'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'thumbnails': item['snippet']['thumbnails'],
            'position': item['snippet']['position'],
        } for item in result['items'] if item['snippet']['resourceId']['kind'] == 'youtube#video'),
    }


def get_video_info(video_id):
    """ Информация о видео """
    result = youtube.request('videos', {
        'id': video_id,
        'part': 'snippet,player',
        'fields': 'items(snippet/title,snippet/description,snippet/thumbnails,player/embedHtml)',
    })

    try:
        item = result['items'][0]
    except (KeyError, IndexError):
        return {}

    return {
        'id': video_id,
        'title': item['snippet']['title'],
        'description': item['snippet']['description'],
        'thumbnails': item['snippet']['thumbnails'],
        'embed': item['player']['embedHtml'],
    }
