import contextlib
import logging

import requests

from promo_util.env_local import (is_prod)
from promo_util.util import (get_api_url, get_access_key)

logger = logging.getLogger('app.api')


class BackendAPI:
    def __init__(self, api_url: str, session: requests.Session):
        self.session = session
        self.api_url = api_url.rstrip('/')
        self.key = None

    def worker_login(self, key: str = None):
        self.key = key or self.key
        r = self.session.post(f'{self.api_url}/Worker/Login', json={
            'accessKey': self.key,
            'seconds': 10 * 60,
        })
        r.raise_for_status()
        self._set_token(r.text)
        return r

    def refresh_token(self):
        logger.debug('Refreshing token')
        r = self.session.post(f'{self.api_url}/Worker/RefreshToken', json={
            'seconds': 10 * 60,
        })
        r.raise_for_status()
        self._set_token(r.text)

    def post(self, path: str, json):
        return self.session.post(f'{self.api_url}{path}', json=json)

    def recreate_images(self, product_id, invalidate=True, only226=False):
        return self.session.post(f'{self.api_url}/Admin/Picture/Recreate', json={
            'id': product_id,
            'invalidateDisabled': not invalidate,
            'only226': only226,
        })

    def post_merchant_center(self, path: str, json=None):
        return self.session.post(f'{self.api_url}/Admin/MerchantCenter/{path}', json=json or dict())

    def get_merchant_center(self, path: str, params=None):
        return self.session.get(f'{self.api_url}/Admin/MerchantCenter/{path}', params=params)

    def create_user(self, data: dict):
        return self.session.post(f'{self.api_url}/Admin/Customer/Create', json=data)

    @classmethod
    @contextlib.contextmanager
    def create_worker(cls, prod=is_prod, key=None, prod_access_key=None):
        with requests.Session() as session:
            api = cls(get_api_url(prod), session)
            key = key or get_access_key(prod_access_key if prod_access_key is not None else prod)
            api.worker_login(key)

            yield api

    def _set_token(self, token: str):
        self.session.headers['Authorization'] = f'Bearer {token}'

    def load_main_categories(self, website, count):
        return self.session.get(f'{self.api_url}/Category/MainCategories', params={
            'website': website,
            'count': count,
        })

    def send_order_email(self, order_id, ):
        return self.session.post(f'{self.api_url}/Admin/Order/SendOrderEmail', json={
            'id': order_id,
            'emailEnabled': True,
        })

    def inspect(self, path, use_cache=False):
        return self.session.get(f'{self.api_url}/Admin/GoogleConsole/Inspect', params={
            'path': path,
            'useCache': use_cache,
        })

    def add_post(self, data):
        return self.session.post(f'{self.api_url}/Admin/Blog/Article/Create', json=data)

    def update_product_slug(self, product_id, slug):
        return self.session.post(f'{self.api_url}/Admin/Product/UpdateSlug', json={
            'invalidateCacheDisabled': True,
            'productId': product_id,
            'slug': slug,
        })
