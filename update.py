import functools
from urllib.parse import urljoin, urlencode

import util.json as json
import util.http as http
import util


__all__ = (
    'update_one'
)


async def update_one(host, index, doc_type, id, body, refresh = False):
    url = build_update_url(host, index, doc_type, id)
    if url is None:
        return None, 'Invalid_Params'

    (status, headers, raw), err = await http.async_request(url, 
        method = 'POST', 
        headers = {"Transfer-Encoding":"identity"}, 
        raw_body_func = functools.partial(json.async_convert_to_json_raw, body))
    if err is not None:
        return None, err

    result, err = parse_update_result(status, headers, raw)
    if err is not None:
        return None, err
    return result, None    


def build_update_url(host, index, doc_type, id):
    if any(x is None for x in (host, index, doc_type, id)):
        return None
    params = dict(
        retry_on_conflict = 5
    )
    return urljoin(host, '%s/%s/%s/_update?%s' % (index, doc_type, id, urlencode(params)))

