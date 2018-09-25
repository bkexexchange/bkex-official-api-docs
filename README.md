# BKEX Official API Document

# HTTP API

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
| orders | String | true | | Order list, **e.g.**, `[{"pair":"BKK_USDT","direction":"BID","price":10,"amount":10}]` |

**NOTE:** The order quantity should be at least one, up to a maximum of 20.

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

# Web Socket API

BASE_END_POINT=wss://ws.bkex.com

命名空间 /quotation


## 1.最新成交

### request

```javascript
[
    "quotationDealConnect",
    {
        "pair": "EOS_USDT", //交易对
    }
]
```

### 全量 response

```javascript
[
    "quotationAllDeal",
    [
        {
            "pair": "EOS_USDT", //交易对
            "p": "0.0018", //价格 price
            "a": 100, //交易量 amount
            "t": 1536995479309, //时间
            "d": "S" //方向 direction
        },
        {
            "pair": "EOS_USDT", //交易对
            "p": "0.0017", //价格 price
            "a": 100, //交易量 amount
            "t": 1536995478065, //时间
            "d": "S" //方向 direction
        },
        {
            "pair": "EOS_USDT", //交易对
            "p": "0.0016", //价格 price
            "a": 100, //交易量 amount
            "t": 1536995476865, //时间
            "d": "S" //方向 direction
        }
    ]
]
```


### 增量 response

```javascript
[
    "quotationListOrder",
    [
         {
            "pair": "EOS_USDT", //交易对
            "p": "0.0016", //价格 price
            "a": 100, //交易量 amount
            "t": 1536995476865, //时间
            "d": "S" //方向 direction
        }
    ]
]
```

d：主动成交方向，S：卖单成交，B：买单成交

## 2.深度

### request

```javascript
[
    "quotationOrderConnect",
    {
        "pair": "EOS_USDT", //交易对
        "number": 50
    }
]
```

### 全量 response

```javascript
[
    "quotationAllOrder",
    [
        {
            "pair": "EOS_USDT", //交易对
            "p": "3521.0000", //价格 price
            "a": 1.0000, //交易量 amount
            "v": 3521.0000, //交易额 volume
            "d": "BID" //方向 direction
        },
        {
            "pair": "EOS_USDT", //交易对
            "p": "3515.0000", //价格 price
            "a": 1.0000, //交易量 amount
            "v": 3515.0000, //交易额 volume
            "d": "BID" //方向 direction
        },
        {
            "pair": "EOS_USDT", //交易对
            "p": "4337.0000", //价格 price
            "a": 1.0000, //交易量 amount
            "v": 3337.0000, //交易额 volume
            "d": "ASK" //方向 direction
        }
    ]
]
```

### 增量 response

```javascript
[
    "quotationListOrder",
    [
        {
            "pair": "EOS_USDT", //交易对
            "p": "140.0000", //价格 price
            "a": -1.000000000000000000, //交易量 amount
            "v": -140.0000000000000000000000, //交易额 volume
            "d": "BID" //方向 direction
        }
    ]
]
```

D：委托方向，S：卖单，B：买单

## 24 小时行情

### request

```javascript
[
    "qAllConnect"
]
```

### response

```javascript
[
    "qPairsStats",
    [
        {
            "pair": "BKK_USDT", //交易对
            "o": 0.0, //开盘价
            "c": 0.0, //收盘价
            "h": 0.0, //最高价
            "l": 0.0, //最低价
            "a": 0.0, //交易量 amount
            "r": 0 //涨跌

        },
        {
            "pair": "BTC_USDT", //交易对
            "o": 1.08, //开盘价
            "c": 1.0, //收盘价
            "h": 353.99, //最高价
            "l": 1.0, //最低价
            "a": 179723.54, //交易量 amount
            "r": -0.07 //涨跌

        }
    ]
]
```

## K 线

### request

```javascript
[
    "quotationConnect",
    {
        "pair": "EOS_USDT", //交易对
        "type": "15", //时间间隔
        "from": 1536142476, //开始时间
        "to": 1537006536, //结束时间
        "no": "153700647609762483" //唯一key
    }
]
```

type 包括 ’1’, '5', '15', '30', '60', '240', '360', '720', '1D', '1W’， 数字表示分钟，1D指一天，1W指一周

### 全量 response 
``` javascript
	
[
    "qPairsAllKLine",
    {
        "no": "153700647609762483",
        "list": [
            {
                "t": 1536636600, //时间
                "c": 990.0, //收盘价
                "o": 10.0, //开盘价
                "h": 990.0, //最高价
                "l": 10.0, //最低价
                "a": 262.25 //交易量 amount
            },
            {
                "t": 1536637500, //时间
                "c": 4990.0, //收盘价
                "o": 10.0, //开盘价
                "h": 4990.0, //最高价
                "l": 10.0, //最低价
                "a": 6165.05 //交易量 amount
            },
            {
                "t": 1536638400, //时间
                "c": 0.0, //收盘价
                "o": 0.0, //开盘价
                "h": 0.0, //最高价
                "l": 0.0, //最低价
                "a": 0.0 //交易量 amount
            }
        ]
    }
]
```

### 增量 response

```javascript
[
    "qPairsKLine",
    {
        "t": 1537005600, //时间
        "c": 0.0018, //收盘价
        "o": 0.0018, //开盘价
        "h": 0.0018, //最高价
        "l": 0.0018, //最低价
        "a": 0.0, //交易量 amount
    }
]
```

## Socket.io Demo(推荐)

```javascript
  var io = require('socket.io-client'); //@1.3.6
  //<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>

  var socket = io('wss://ws.bkex.com/quotation', { transports: ['websocket'] });
  
  socket.on('connect', function (data) {
    socket.emit('qAllConnect'); //获取24小时行情
  });
  
```

## Native WebScokdt Demo

```javascript
    var pingPong = null;
    ws = new WebSocket("wss://ws.bkex.com/socket.io/?EIO=3&transport=websocket");
    ws.onopen = function() {
      pingPong = setInterval(function () { //跟服务端ping pong 保持连接额状态
        ws.send('2');
      }, 20 * 1000)

    };
    ws.onmessage = function(e) {
        
        if(e.data === '40') { //链接成功
          ws.send('40/quotation')
        }

        else if(e.data === '40/quotation') { //进入命名空间成功
          ws.send('42/quotation,["quotationConnect",{"pair": "EOS_USDT","type": "15","from": 1536142476,"to": 1537865828,"no": "153700647609762483"}]')
        } 
        
        else { //其他消息
          
        }
    };

```



