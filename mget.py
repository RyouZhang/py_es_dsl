import functools
from urllib.parse import urljoin, urlencode


__all__ = (
    'build_mget'
)

async def build_mget(host, index, doc_type, ids, include_fields = None, exclude_fields = None):
    if ids is None or len(ids) <= 0:
        return None, 'Invalid_Params'
    
    if any(x is None for x in (host, index, doc_type)):
        return None, 'Invalid_Params'

    params = dict()
    if exclude_fields is not None:
        params['_source_exclude'] = ','.join(exclude_fields)
    if include_fields is not None:
        params['_source_include'] = ','.join(include_fields)

    url = urljoin(host, '%s/%s/_mget?%s' % (index, doc_type, urlencode(params)))

    body = dict(ids = ids)

    return url, body