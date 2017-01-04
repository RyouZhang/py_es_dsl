import functools
from urllib.parse import urljoin, urlencode


__all__ = (
    'build_get_url'
)


def build_get_url(host, index, doc_type, id, include_fields = None, exclude_fields = None):
    if any(x is None for x in (host, index, doc_type, id)):
        return None

    params = dict()
    if exclude_fields is not None:
        params['_source_exclude'] = ','.join(exclude_fields)
    if include_fields is not None:
        params['_source_include'] = ','.join(include_fields)

    return urljoin(host, '%s/%s/%s/_source?%s' % (index, doc_type, id, urlencode(params)))


