# BKEX Official API Document
### API服务域名：

BASE_END_POINT=https://api.bkex.com



### 加密过程

假设用户申请得到的API key信息如下：

secretKey:  NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j

accessKey: vmsUZE6mv9SD5VNak4HlWFsOr6aKE2zvsw0MuIgwCIGy6utIco14y7Ju91duEh82



以以下请求为例

```json
curl -X GET \
  'http://<BASE_END_POINT>/v1/q/depth?&precision=2&pair=ETH_USDT' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'X_ACCESS_KEY: vmsUZE6mv9SD5VNak4HlWFsOr6aKE2zvsw0MuIgwCIGy6utIco14y7Ju91duEh82' \
  -H 'X_SIGNATURE: 550ac73ace8c34372e0e1dd6631e890c7bd16697af8bb4e2908e966b50aba4e0' \
```

- 首先对请求参数的key进行ASCII排列得到结果 ```pair=ETH_USDT&precision=2```  
- 然后使用secretKey 进行HMAC SHA256进行加密

```shell
[linux]$ echo -n "pair=ETH_USDT&precision=2" | openssl dgst -sha256 -hmac "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
```

得到的内容是 ``` 550ac73ace8c34372e0e1dd6631e890c7bd16697af8bb4e2908e966b50aba4e0```

- 构造http请求:  使用  ```X_ACCESS_KEY``` 这个header存储access key信息，  使用``` X_SIGNATURE``` header 存储第二步生成的签名信息， 然后发送http请求



## Quotation API
### Get quotation depth
```
GET /v1/q/depth
```
Parameters:

| Name | Type | Required | Default | Description  |
| ---- | ---- | -------- | ------- | ------------ |
| pair | STRING | true | | |
| size | INT | false | 50 | |
| precision | INT | false | | |

Response:
```json
{
  "msg": "success",
  "code": 0,
  "data": {
    "asks": [
      {
        "pair": "ETH_USDT",
        "direction": "ASK",
        "amt": 50,
        "price": 1.32
      },
      {
        "pair": "ETH_USDT",
        "direction": "ASK",
        "amt": 40,
        "price": 2.32
      }
    ],
    "bids": [
      {
        "pair": "ETH_USDT",
        "direction": "BID",
        "amt": 1250,
        "price": 1.12
      },
      {
        "pair": "ETH_USDT",
        "direction": "BID",
        "amt": 160,
        "price": 1.11
      }
    ]
  }
}
```

- asks : 卖单构成的数组

  bids: 买单构成的数组

- 单个买卖单

  direction:   BID-- 买单  ASK-卖单

  amt:    该价格下总量

  price: 价格参数



### Get quotation deals
```
GET /v1/q/deals
```
Parameters:

| Name | Type | Required | Default | Description  |
| ---- | ---- | -------- | ------- | ------------ |
| pair | STRING | true | | |
| size | INT | false | 20 | |

Response:
``` json
{
  "msg": "success",
  "code": 0,
  "data": [
    {
      "pair": "ETH_USDT",
      "dealAmount": 10,
      "price": 1.3236,
      "createdTime": 1532190888913,
      "tradeDealDirection": "B"
    },
    {
      "pair": "ETH_USDT",
      "dealAmount": 10,
      "price": 1.3236,
      "createdTime": 1532190887795,
      "tradeDealDirection": "B"
    },
    {
      "pair": "ETH_USDT",
      "dealAmount": 10,
      "price": 1.3235,
      "createdTime": 1532190886739,
      "tradeDealDirection": "B"
    },
    {
      "pair": "ETH_USDT",
      "dealAmount": 10,
      "price": 1.3235,
      "createdTime": 1532190862672,
      "tradeDealDirection": "B"
    },
    {
      "pair": "ETH_USDT",
      "dealAmount": 10,
      "price": 1.3234,
      "createdTime": 1532190862398,
      "tradeDealDirection": "B"
    }
  ]
}
```

- pair: 交易对

  dealAmount: 成交量

  price: 成交价格

  createTime: 成交时间

  tradeDealDirection: 主动成交方向。 主动成交方向，如果是主动发起买单成交，代表外盘，值是B， 如果是主动卖单来成交，代表内盘，值是S



## Trade API
### Get all unfinished order
```
GET /v1/u/trade/order/listUnfinished
```
Parameters:

| Name | Type | Required | Default | Description  |
| ---- | ---- | -------- | ------- | ------------ |
| page | INT | false | 1 | Page number. |
| size | INT | false | 10 | Page size, max 100. |
| pair | STRING | true | | Trade pair, **e.g.**, `BTC_USDT`. |
| direction | STRING | false | | Trade direction, `BID` or `ASK`. |

Response:
``` json
{
  "code": 0,
  "data": {
    "data":[
      {
        "createdTime": 1532177952546,
        "dealAmount": 0,
        "dealAvgPrice": 0,
        "direction": "ASK",
        "frozenAmountByOrder": 10,
        "id": "2018072120591254687003222",
        "orderType": "LIMIT",
        "pair": "BKK_USDT",
        "price": 0.12,
        "status": 0,
        "totalAmount": 10,
        "updateTime": null
      }
    ],
    "pageRequest": {
      "page": 1, 
      "size": 100, 
      "orderBy": "id", 
      "asc": false
    },
    "total": 1
  },
  "msg": "success"
}
```

### Get all finished order
```
GET /v1/u/trade/order/history
```
<strong>NOTE:</strong> Default duration is 3 days, and max duration is 7 days.

Parameters:

| Name | Type | Required | Default | Description  |
| ---- | ---- | -------- | ------- | ------------ |
| page | INT | false | 1 | Page number. |
| size | INT | false | 10 | Page size, max 100. |
| startTime | LONG | false | | Order start time. |
| endTime | LONG | false | | Order finish time. |
| pair | STRING | true | | Trade pair, <strong>e.g.</strong>, `BTC_USDT`. |
| direction | STRING | false | | Trade direction, `BID` or `ASK`. |

Response:
```json
{
  "code": 0,
  "data": {
    "data":[
      {
        "createdTime": 1532177952546,
        "dealAmount": 0,
        "dealAvgPrice": 0,
        "direction": "ASK",
        "frozenAmountByOrder": 10,
        "id": "2018072120591254687003222",
        "orderType": "LIMIT",
        "pair": "BKK_USDT",
        "price": 0.12,
        "status": 0,
        "totalAmount": 10,
        "updateTime": 1532177952546
      }
    ],
    "pageRequest": {
      "page": 1, 
      "size": 100, 
      "orderBy": "id", 
      "asc": false
    },
    "total": 1
  },
  "msg": "success"
}
```

### Create new order
```
POST /v1/u/trade/order/create
```
Parameters:

| Name | Type | Required | Default | Description  |
| ---- | ---- | -------- | ------- | ------------ |
| pair | STRING | true | | Trade pair, **e.g.**, `BTC_USDT`. |
| direction | STRING | false | | Trade direction, `BID` or `ASK`. |
| price | DECIMAL | true | | Order price. |
| amount | DECIMAL | true | | Order amount. |

Response:
```json
{
  "code": 0,
  "data": "2018072120591254687003222",
  "msg": "success"
}
```

### Cancel order
```
POST /v1/u/trade/order/cancel
```
Parameters:

| Name | Type | Required | Default | Description  |
| ---- | ---- | -------- | ------- | ------------ |
| pair | STRING | true | | Trade pair, **e.g.**, `BTC_USDT`. |
| orderNo | STRING | true | | Order id. |

Response:
```json
{
  "code": 0,
  "data": "2018072120591254687003222",
  "msg": "success"
}
```

### Get unfinished order detail
```
GET /v1/u/trade/order/unfinished/detail
```
Parameters:

| Name | Type | Required | Default | Description  |
| ---- | ---- | -------- | ------- | ------------ |
| pair | STRING | true | | Trade pair, **e.g.**, `BTC_USDT`. |
| orderNo | STRING | true | | Order id. |

Response:
```
{
  code: 0,
  data: {
    createdTime: 1532177952546,
    dealAmount: 0,
    dealAvgPrice: 0,
    direction: "ASK",
    frozenAmountByOrder: 10,
    id: "2018072120591254687003222",
    orderType: "LIMIT",
    pair: "BKK_USDT",
    price: 0.12,
    status: 0,
    totalAmount: 10,
    updateTime: null
  },
  msg: "success"
}
```

### Get finished order detail
```
GET /v1/u/trade/order/finished/detail
```
Parameters:

| Name | Type | Required | Default | Description  |
| ---- | ---- | -------- | ------- | ------------ |
| orderNo | STRING | true | | Order id. |
| updateTime | LONG | true | | Order update time. |

Response:
```json
{
  "code": 0,
  "data": {
    "createdTime": 1532177952546,
    "dealAmount": 0,
    "dealAvgPrice": 0,
    "direction": "ASK",
    "frozenAmountByOrder": 10,
    "id": "2018072120591254687003222",
    "orderType": "LIMIT",
    "pair": "BKK_USDT",
    "price": 0.12,
    "status": 0,
    "totalAmount": 10,
    "updateTime": null
  },
  "msg": "success"
}
```

### Batch create new order
```
POST /v1/u/trade/order/batchCreate
```
Parameters:

| Name | Type | Required | Default | Description  |
| ---- | ---- | -------- | ------- | ------------ |
| pair | STRING | true | | Trade pair, **e.g.**, `BTC_USDT`. |
| direction | STRING | true | | Trade direction, `BID` or `ASK`. |
| price | DECIMAL | true | | Order price. |
| amount | DECIMAL | true | | Order amount. |
| size | INT | true | | Order size, max 20. |

Response:
```json
{
  "code": 0,
  "data": {
    "success": 2,
    "fail": 0,
    "results": [
      "2018072120591254687003222",
      "2018072120591254687003223"
    ]
  },
  "msg": "success"
}
```

### Batch cancel order
```
POST /v1/u/trade/order/batchCancel
```
Parameters:

| Name | Type | Required | Default | Description  |
| ---- | ---- | -------- | ------- | ------------ |
| orders | ARRAY | true | | Order list, **e.g.**,  
||||| `[` |
|||||   `{` |
|||||     `"id": "2018072120591254687003222",` |
|||||     `"pair": "BKK_USDT"` |
|||||   `}` |
||||| `]` |

Response:
```json
{
  "code": 0,
  "data": {
    "success": 2,
    "fail": 0,
    "results": [
      "2018072120591254687003222", 
      "2018072120591254687003223"
    ]
  },
  "msg": "success"
}
```

### Batch cancel order by pair
```
POST /v1/u/trade/order/batchCancelByPair
```
Parameters:


| Name | Type | Required | Default | Description  |
| ---- | ---- | -------- | ------- | ------------ |
| pair | STRING | true | | Trade pair, **e.g.**, `BTC_USDT`. |

Response:
```json
{
  "code": 0,
  "data": {
    "success": 2,
    "fail": 0,
    "results": [
      "2018072120591254687003222", 
      "2018072120591254687003223"
    ]
  },
  "msg": "success"
}
```

## Wallet API
### Get user account balance
```
GET /v1/u/wallet/balance
```
Parameters:

| Name | Type | Required | Default | Description  |
| ---- | ---- | -------- | ------- | ------------ |
| coinTypes | STRING | false | | Coin type separate by `,`, **e.g.**, `BTC`, `BTC,USDT`.

Response:
```json
{
  "code": 0,
  "data": [
    {
      "coinType": "BTC",
      "available": 1,
      "frozen": 0,
      "total": 1
    }
  ],
  "msg": "success"
}
```
