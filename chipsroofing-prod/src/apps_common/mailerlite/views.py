from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from .models import RegularCampaign
from .utils import fill_demo

# TODO: не только для RegularCampaign


def preview_campaign(request, campaign_id):
    from premailer import Premailer
    campaign = get_object_or_404(RegularCampaign, pk=campaign_id)
    content = campaign.final_html(request)
    content = fill_demo(content)
    content = Premailer(content, strip_important=False).transform()
    return HttpResponse(content)


def preview_campaign_plain(request, campaign_id):
    campaign = get_object_or_404(RegularCampaign, pk=campaign_id)
    content = campaign.final_plain(request)
    content = fill_demo(content)
    return HttpResponse('<pre>%s</pre>' % content.strip())
