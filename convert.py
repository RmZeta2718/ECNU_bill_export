import yaml
from datetime import datetime, timedelta
from objprint import op

def ParseConfig(config_file: str='config.yaml') -> dict[str, dict]:
    with open(config_file, 'r', encoding='utf-8') as f:
        conf = yaml.safe_load(f)
        # op(conf)
    meta = {}
    for item in conf['convert']:
        for shop in item['shop']:
            assert shop not in meta, op(f"{shop} duplicated")
            meta[shop] = {
                'type': item['type'],
                'detail': item['detail'] if 'detail' in item else False,
                'ignore': False,
            }
    for shop in conf['ignore']:
        meta[shop] = {'ignore': True}
    return meta

# coalesce amount if interval < 1hour and have the same type and comment
def Coalesce(data: list[dict]):
    def str2time(s: str) -> datetime:
        return datetime.strptime(s, '%Y-%m-%d %H:%M')
    def equal(lhs: dict, rhs: dict) -> bool:
        if lhs['type'] != rhs['type'] or lhs['comment'] != rhs['comment']:
            return False
        return str2time(rhs['time']) - str2time(lhs['time']) < timedelta(hours=1)

    data.sort(key=lambda item: item['time'])
    rst = []
    for idx in range(1, len(data)):
        if equal(data[idx - 1], data[idx]):
            rst[-1]['amount'] += data[idx]['amount']
        else:
            rst.append(data[idx])
    return rst

def Convert(data: list[dict], meta: dict[str, dict]):
    rst = []
    notfound = set()
    for item in data:
        if item['shopname'] not in meta:
            notfound.add(item['shopname'])
            continue

        item_meta = meta[item['shopname']]
        if item_meta['ignore']:
            continue

        time_list = list(item['time'][:-2])
        time_list.insert(10, ':')
        time_list.insert(8, ' ')
        time_list.insert(6, '-')
        time_list.insert(4, '-')

        new_item = {
            'amount': item['amount'],
            'type': item_meta['type'],
            'comment': item['shopname'],
            'time': ''.join(time_list),
        }

        if item_meta['detail']:
            termname:str = item['termname']
            termname = termname[:termname.rfind('-')]  # remove -13 suffix in termname
            new_item['comment'] += f"@{termname}"
        
        rst.append(new_item)

    rst = Coalesce(rst)

    return rst, notfound


if __name__ == '__main__':
    op.config(color=True, line_number=True, arg_name=True)
    meta = ParseConfig()
    with open('dump.json', 'r') as f:
        import json
        data = json.loads(f.read())
    data, notfound = Convert(data, meta)
    # op(data, notfound)
    # op(notfound)
    print(json.dumps(data, ensure_ascii=False))