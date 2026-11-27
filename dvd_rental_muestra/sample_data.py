"""Create a reproducible, relationally consistent DVD rental demo sample."""
from pathlib import Path
import argparse
import shutil
import pandas as pd

SEED = 42
LIMIT = 500
UNCHANGED = ['actors.csv', 'address_cust.csv', 'category.csv', 'customer.csv', 'film.csv', 'language.csv']

def build(raw, output):
    raw, output = Path(raw), Path(output)
    if raw.resolve() == output.resolve():
        raise ValueError('Use a separate output directory to preserve RAW data.')
    output.mkdir(parents=True, exist_ok=True)
    rental = pd.read_csv(raw / 'rental.csv')
    payment = pd.read_csv(raw / 'paymnet.csv')
    inventory = pd.read_csv(raw / 'inventory.csv')
    film_actor = pd.read_csv(raw / 'film_actor.csv')
    sampled_rental = rental.sample(n=LIMIT, random_state=SEED).sort_values('rental_id')
    sampled_payment = payment[payment.rental_id.isin(sampled_rental.rental_id)].copy()
    if len(sampled_payment) != LIMIT:
        raise ValueError('Selected rentals do not have exactly 500 linked payments.')
    required_inventory = inventory[inventory.inventroy_id.isin(sampled_rental.inventory_id)]
    extra_inventory = inventory[~inventory.inventroy_id.isin(required_inventory.inventroy_id)].sample(n=LIMIT-len(required_inventory), random_state=SEED)
    sampled_inventory = pd.concat([required_inventory, extra_inventory]).sort_values('inventroy_id')
    # Give films represented in sampled rentals a chance to retain an actor link.
    candidates = film_actor[film_actor.film_id.isin(required_inventory.film_id)]
    required_links = candidates.sample(frac=1, random_state=SEED).drop_duplicates('film_id')
    extra_links = film_actor.drop(index=required_links.index).sample(n=LIMIT-len(required_links), random_state=SEED)
    sampled_links = pd.concat([required_links, extra_links]).sort_values(['film_id','actor_id'])
    assert set(sampled_rental.inventory_id) <= set(sampled_inventory.inventroy_id)
    assert set(sampled_payment.rental_id) == set(sampled_rental.rental_id)
    assert sampled_payment.merge(sampled_rental, on='rental_id').eval('customer_id_x == customer_id_y').all()
    for name, frame in [('rental.csv', sampled_rental), ('paymnet.csv', sampled_payment.sort_values('payment_id')), ('inventory.csv', sampled_inventory), ('film_actor.csv', sampled_links)]:
        assert len(frame) == LIMIT
        frame.to_csv(output / name, index=False)
    for name in UNCHANGED:
        shutil.copyfile(raw / name, output / name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('raw', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    build(args.raw, args.output)
