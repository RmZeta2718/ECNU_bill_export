import pandas as pd

def Export(data: list[dict], out_file='out/dump.csv'):
    df = pd.DataFrame([{
        '时间': item['time'],
        '分类': item['type'],
        '类型': '支出',
        '金额': item['amount'],
        '账户1': '',
        '账户2': '',
        '备注': item['comment'],
        '账单标记': '',
        '账单图片': '',
    } for item in data])
    df.sort_values('时间', inplace=True)

    df.to_csv(out_file, index=False, encoding='utf-8')
