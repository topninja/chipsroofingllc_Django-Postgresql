import requests
from django.views.generic import View
from django.shortcuts import redirect, resolve_url
from django.http.response import Http404, HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import add_message, SUCCESS
from libs.views_ajax import AdminViewMixin
from .models import SocialConfig


class TwitterTokenView(AdminViewMixin, View):
    def get(self, request, *args, **kwargs):
        from requests_oauthlib import OAuth1Session

        config = SocialConfig.get_solo()
        oauth_token = request.GET.get('oauth_token')
        oauth_verifier = request.GET.get('oauth_verifier')

        oauth_client = OAuth1Session(
            client_key=config.twitter_client_id,
            client_secret=config.twitter_client_secret,
            resource_owner_key=oauth_token,
            resource_owner_secret=config.twitter_access_token_secret,
            verifier=oauth_verifier
        )

        try:
            answer = oauth_client.fetch_access_token('https://api.twitter.com/oauth/access_token')
        except ValueError:
            raise Http404

        if answer and 'oauth_token' in answer:
            SocialConfig.objects.update(twitter_access_token=answer['oauth_token'])
            add_message(request, SUCCESS, _('Twitter access_token updated successfully!'))
            return redirect('admin:social_networks_socialconfig_change')
        else:
            return HttpResponse(answer)


class FacebookTokenView(AdminViewMixin, View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', '')
        if not code:
            raise Http404

        config = SocialConfig.get_solo()
        redirect_uri = self.request.build_absolute_uri(resolve_url('admin_social_networks:facebook_token'))
        response = requests.get(
            'https://graph.facebook.com/oauth/access_token',
            params={
                'client_id': config.facebook_client_id,
                'client_secret': config.facebook_client_secret,
                'redirect_uri': redirect_uri,
                'code': code,
                'type': 'web_server',
            }
        )

        short_token = response.json()['access_token']
        response = requests.get(
            'https://graph.facebook.com/oauth/access_token',
            params={
                'grant_type': 'fb_exchange_token',
                'client_id': config.facebook_client_id,
                'client_secret': config.facebook_client_secret,
                'fb_exchange_token': short_token,
            }
        )

        long_token = response.json()['access_token']
        response = requests.get(
            'https://graph.facebook.com/me/accounts',
            params={
                'access_token': long_token,
            }
        )

        answer = response.json()
        if answer and ('data' in answer) and ('access_token' in answer['data'][0]):
            SocialConfig.objects.update(facebook_access_token=answer['data'][0]['access_token'])
            add_message(request, SUCCESS, _('Facebook access_token updated successfully!'))
            return redirect('admin:social_networks_socialconfig_change')
        else:
            return HttpResponse(response.text)


class InstagramTokenView(AdminViewMixin, View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', '')
        if not code:
            raise Http404

        config = SocialConfig.get_solo()
        redirect_uri = self.request.build_absolute_uri(resolve_url('admin_social_networks:instagram_token'))
        response = requests.post(
            'https://api.instagram.com/oauth/access_token',
            data={
                'grant_type': 'authorization_code',
                'client_id': config.instagram_client_id,
                'client_secret': config.instagram_client_secret,
                'redirect_uri': redirect_uri,
                'code': code,
            }
        )

        answer = response.json()
        if answer and 'access_token' in answer:
            SocialConfig.objects.update(instagram_access_token=answer['access_token'])
            add_message(request, SUCCESS, _('Instagram access_token updated successfully!'))
            return redirect('admin:social_networks_socialconfig_change')
        else:
            return HttpResponse(response.text)


class LinkedinTokenView(AdminViewMixin, View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', '')
        if not code:
            raise Http404

        config = SocialConfig.get_solo()
        redirect_uri = self.request.build_absolute_uri(resolve_url('admin_social_networks:linkedin_token'))
        response = requests.post(
            'https://www.linkedin.com/oauth/v2/accessToken',
            data={
                'grant_type': 'authorization_code',
                'client_id': config.linkedin_client_id,
                'client_secret': config.linkedin_client_secret,
                'redirect_uri': redirect_uri,
                'code': code,
            }
        )

        answer = response.json()
        if answer and 'access_token' in answer:
            SocialConfig.objects.update(linkedin_access_token=answer['access_token'])
            add_message(request, SUCCESS, _('LinkedIn access_token updated successfully!'))
            return redirect('admin:social_networks_socialconfig_change')
        else:
            return HttpResponse(response.text)
