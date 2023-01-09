# ECNU bill export

ECNU ECard 账单导出为[钱迹](https://www.qianjiapp.com/)格式。

# Usage

- `cp config.py.example config.py`
- 抓包得到 header 中的 `sw-Authorization` ，填入 <u>config.py</u>
- `./main.py --year 2022`
- 导出文件： <u>out/dump.csv</u> 

其他命令行参数见 `./main.py -h`

## 原理

- 数据获取：通过小程序抓包获得session key （参考[woria的博客](https://www.woria.xyz/2021/11/02/ECNU%E6%89%93%E5%8D%A1/)），然后直接批量发起HTTP POST请求获取数据。
  - 需要注意的是，最近Win上无法抓包了，但是Mac上可以
- 格式转换：做简单处理后生成目标格式的csv即可。
  - 转换的配置在 <u>config.yaml</u>

## 配置

### convert

| 参数 | 类型 | 描述 |
|---|---|---|
| type | str | 这一组对应的导出类型 |
| shop | list[str] | 来自ECard账单的一组消费位置 |
| detail | bool | 是否要在备注中加上POS机位置，可选，默认False |

### ignore

忽略的shop列表
