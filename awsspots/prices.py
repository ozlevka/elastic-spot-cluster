from pyquery import PyQuery
import urllib3
import json
import os


INSTANCES_SPOT_INSTANCE_URL = "http://spot-price.s3.amazonaws.com/spot.js"
AMAZON_TYPES_URL='https://aws.amazon.com/ec2/instance-types/'
USE_CACHE = True

if 'USE_CACHE' in os.environ:
    USE_CACHE = os.environ['USE_CACHE'] == 'True'

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

        if USE_CACHE:
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
    if USE_CACHE and os.path.exists('./prices_cache.json'):
        with open('./prices_cache.json', mode="r") as file:
            return json.load(file)
    else:
        pool = urllib3.PoolManager()
        response = pool.request('GET', INSTANCES_SPOT_INSTANCE_URL)
        txt = response.data.decode('UTF-8')
        txt = txt.replace('callback(', '')
        txt = txt[:len(txt) - 2]
        if USE_CACHE:
            with open('./prices_cache.json', mode='w') as file:
                file.write(txt)
        return json.loads(txt)



def lambda_handler(event, context):
    instances = get_amazon_types()
    prices = get_prices()
    append_region_prices(instances, prices)

    cpu = 0
    memory = 0

    if 'cpu' in event:
        cpu = event['cpu']

    if 'memory' in event:
        memory = event['memory']

    ret_object = instances

    if cpu > 0:
        ret_object = [inst for inst in instances if 'cpu' in inst and (inst['cpu'] >= cpu)]

    if memory > 0:
        ret_object = [inst for inst in ret_object if 'memory' in inst and (inst['memory'] >= (memory -2) and inst['memory'] <= (memory + 2))]

    return {
        'statusCode': 200,
        'body': json.dumps(ret_object)
    }



def main():
    instances = get_amazon_types()
    prices = get_prices()
    append_region_prices(instances, prices)





if __name__ == '__main__':
    main()