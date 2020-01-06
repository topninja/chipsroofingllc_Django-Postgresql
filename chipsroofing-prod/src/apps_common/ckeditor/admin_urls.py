from django.conf.urls import url
from . import admin

urlpatterns = [
    url(r'^pagephoto/upload/$', view=admin.upload_pagephoto, name='upload_pagephoto'),
    url(r'^pagephoto/rotate/$', view=admin.rotate_pagephoto, name='rotate_pagephoto'),
    url(r'^pagephoto/crop/$', view=admin.crop_pagephoto, name='crop_pagephoto'),
    url(r'^pagefile/upload/$', view=admin.upload_pagefile, name='upload_pagefile'),
    url(r'^simplephoto/upload/$', view=admin.upload_simplephoto, name='upload_simplephoto'),
]
