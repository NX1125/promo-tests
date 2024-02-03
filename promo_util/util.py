import datetime
from pathlib import Path

from promo_util.env_local import is_prod


def utcnow():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)


def get_api_url(prod: bool = is_prod):
    return (
        'http://localhost:5000',
        'https://api.promowe.com/',
    )[prod]


def get_access_key(prod: bool = is_prod):
    ext = 'prod' if prod else 'dev'
    with open(Path(__file__).parent.with_name(f'.worker_access_key.{ext}.txt'), 'r', encoding='utf-8') as file:
        return file.read().strip()
