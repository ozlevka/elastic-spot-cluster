from pyquery import PyQuery
import urllib3
import json
import os


INSTANCES_SPOT_INSTANCE_URL = "http://spot-price.s3.amazonaws.com/spot.js"
AMAZON_TYPES_URL='https://aws.amazon.com/ec2/instance-types/'
USE_CACHE = True

if 'USE_CACHE' in os.environ:
    USE_CACHE = bool(os.environ['USE_CACHE'])

def get_amazon_types():
    if USE_CACHE and os.path.exists('./types_cashe.json'):
        with open('./types_cashe.json', mode='r') as file:
            return json.load(file)
    else:
        data = []
        walker = PyQuery(url=AMAZON_TYPES_URL)
        all_table = walker('div.row-builder div.table-wrapper table')
        for tr in all_table.items(selector='tr'):
            items = []
            counter = 0
            for td in tr.items(selector='td'):
                if "Instance" in td.text() or td.text() == 'Yes':
                    break
                else:
                    if counter > 2:
                        if len(items) > 0:
                            data.append(dict(
                                name=items[0],
                                cpu=int(items[1].replace('**', '')),
                                memory=float(items[2].replace(',', ''))
                        ))
                        counter = 0
                        break
                    items.append(td.text())
                    counter += 1



            a = 'b'

        with open('./types_cashe.json', mode='w') as file:
            json.dump(data, file)
        return data


def append_region_prices(instances, prices):
    for region in prices['config']['regions']:
        for type in region['instanceTypes']:
            for inst in type['sizes']:
                record = [t for t in instances if t['name'] == inst['size']]
                if len(record) > 0:
                    record[0][region['region']] = dict(
                        prices=inst['valueColumns']
                    )
                else:
                    item = dict(
                        name=inst['size']
                    )
                    item[region['region']] = dict(
                        prices=inst['valueColumns']
                    )
                    instances.append(item)

def get_prices():
    if USE_CACHE and not os.path.exists('./prices_cache.json'):
        pool = urllib3.PoolManager()
        response = pool.request('GET', INSTANCES_SPOT_INSTANCE_URL)
        txt = response.data.decode('UTF-8')
        txt = txt.replace('callback(', '')
        txt = txt[:len(txt) - 2]
        with open('./prices_cache.json', mode='w') as file:
            file.write(txt)
        return json.loads(txt)
    else:
        with open('./prices_cache.json', mode="r") as file:
            return json.load(file)



def main():
    instances = get_amazon_types()
    prices = get_prices()
    append_region_prices(instances, prices)





if __name__ == '__main__':
    main()