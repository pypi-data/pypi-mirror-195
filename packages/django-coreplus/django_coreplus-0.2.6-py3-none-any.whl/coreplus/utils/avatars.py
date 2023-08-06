import hashlib
import os
import uuid

from django.utils.http import urlencode


def upload_avatar_to(instance, filename, uid=None):
    filename, ext = os.path.splitext(filename)
    uid = uid or uuid.uuid4()
    return os.path.join(
        "avatar_images",
        "avatar_{uuid}_{filename}{ext}".format(
            uuid=uid,
            filename=filename,
            ext=ext,
        ),
    )


def get_gravatar_url(email, size=50):
    default = "mm"
    size = (
        int(size) * 2
    )  # requested at retina size by default and scaled down at point of use with css
    gravatar_provider_url = "//www.gravatar.com/avatar"

    if (not email) or (gravatar_provider_url is None):
        return None

    gravatar_url = "{gravatar_provider_url}/{hash}?{params}".format(
        gravatar_provider_url=gravatar_provider_url.rstrip("/"),
        hash=hashlib.md5(email.lower().encode("utf-8")).hexdigest(),
        params=urlencode({"s": size, "d": default}),
    )
    return gravatar_url
