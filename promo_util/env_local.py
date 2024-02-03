from pathlib import Path

with open(Path(__file__).parent.with_name('.env'), 'r', encoding='utf-8') as file:
    prod = file.read().strip() == 'prod'

is_prod = prod
