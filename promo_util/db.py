import contextlib
import enum

import psycopg2

from promo_util.env_local import is_prod

prod_host = 'promowe3-db.cdmgoaih5hxe.us-east-1.rds.amazonaws.com'

class Website(enum.Enum):
    ppi = 'promotional_product_inc'
    pw = 'promo_we'


db_names = (
    {  # dev
        Website.ppi: 'ppidb',
        Website.pw: 'promowedb4',
    },
    {  # prod
        Website.ppi: 'ppidb',
        Website.pw: 'promowedb',
    },
)


def create_connection(website: Website, prod: bool = is_prod, port=5432, host=None):
    return psycopg2.connect(
        dbname=db_names[prod][website],
        user='postgres' if prod else 'dev_user',
        host=host or (prod_host if prod else 'localhost'),
        port=port,
    )


@contextlib.contextmanager
def connect(website: Website, prod: bool = is_prod, port=5432, host=None):
    with create_connection(website, prod, port, host) as conn:
        yield conn


@contextlib.contextmanager
def connect_tunnel(website: Website):
    """
    localhost:5050
    """
    # tunnel = subprocess.Popen(['sh', Path(__file__).parent.parent / 'tunnel.sh'])
    # try:
    with create_connection(website, prod=True, host='localhost', port=5050) as conn:
        yield conn
    # finally:
    #     tunnel.terminate()
    #     tunnel.wait()


@contextlib.contextmanager
def connect_or_tunnel(tunnel, website: Website):
    with (
            connect_tunnel(website)
            if tunnel
            else connect(website, prod=True, port=5432, host=prod_host)
    ) as conn:
        yield conn
