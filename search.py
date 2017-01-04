import functools
from urllib.parse import urljoin, urlencode

import util.json as json
import util.http as http
import util


__all__ = (
    'search',
    'ESSearchBody',
)

class ESSearchBody(dict):

    def __init__(self, query):
        super(ESSearchBody, self).__init__()
        self['query'] = query

    def orderby_score(self):
        sort = self.get('sort', [])
        sort.append('_score')
        self['sort'] = sort
        return self
    
    def orderby(self, field, order='asc'):
        sort = self.get('sort', [])

        temp = {}
        temp[field] = dict(order=order)

        sort.append(temp)
        self['sort'] = sort
        return self
    
    def orderby_distance(self, field, center, order='asc'):
        sort = self.get('sort', [])

        temp = {'_geo_distance': {}}
        temp['_geo_distance'][field] = center
        temp['_geo_distance']['order'] = order

        sort.append(temp)
        self['sort'] = sort
        return self
    
    def source_hide(self):
        self['_source'] = False
        return self

    def source_include(self, fields=None, old_mode=False):
        source = self.get('_source', dict())
        if old_mode:
            source['include'] = fields
        else:
            source['includes'] = fields
        self['_source'] = source
        return self
    
    def source_exclude(self, fields=None, old_mode=False):
        source = self.get('_source', dict())
        if old_mode:
            source['exclude'] = fields
        else:
            source['excludes'] = fields
        self['_source'] = source
        return self        
    
    def page_range(self, from_index=0, size=10):
        self['from'] = from_index
        self['size'] = size
        return self
    
    def aggregation(self, name, aggr):
        aggs = self.get('aggs', dict())
        aggs[name] = aggr
        self['aggs'] = aggs
        return self


async def search(host, index, doc_type, params = None, body = None):
    url = build_search_url(host, index, doc_type, params)
    if url is None:
        
        return None, 'Invalid_Params'

    (status, headers, raw), err = await http.async_request(url, 
        method = 'POST', 
        headers = {"ransfer-Encoding":"identity"}, 
        raw_body_func = functools.partial(json.async_convert_to_json_raw, body))

    if err is not None:
        return None, err
    
    result, err = parse_search_result(status, headers, raw)
    if err is not None:
        return None, err
    return result, None  


def build_search_url(host, index, doc_type, params = None):
    if any(x is None for x in (host)):
        return None
    if doc_type and index is None:
        index = '_all'

    if params is not None:
        return urljoin(host, '%s/%s/_search?%s' % (index, doc_type, urlencode(params)))
    else:
        return urljoin(host, '%s/%s/_search' % (index, doc_type))
