# HungryOsori-TestServer
[HungryOsori-iOS](https://github.com/HyOsori/HungryOsori-iOS) 클라이언트를 개발하다가, 서버가 필요해서 급히 만들었다. 실제 서버는 Django로 만들어질 예정. 테스트 서버라 DB연동도 없고, 데이터도 고정적이다.
사용자 정보는 메모리에 잠시 저장하기 때문에, 서버를 내렸다 올리면 리셋된다.

# Installation & Run
```
git clone https://github.com/HyOsori/HungryOsori-TestServer.git
python ./HungryOsori-TestServer/app.py
```

# API
### 1. Login
- /req_login

|Data|Description|
|----|-----------|
|user_id|사용자 아이디|
|user_key|서버에서 발급하는 키, user_key없이 request를 날리면, 서버에서 key를 발급한다.|
|user_pw|사용 안함|
|token|Push Token(FCM Device ID), 없을 경우 key를 아예 안 넣어주면 된다.|

- Response
```JSON
{
  "user_key": "nu8qdEnCTDC96hLbmwhodg",
 "message": "Success",
  "error": 0
}
```

### 2. Crawler Entire List
- /req_entire_list

|Data|Description|
|----|-----------|
|user_id|사용자 아이디|
|user_key|서버에서 발급받은 키, user_key없이 request를 날리면 <B>에러</B>가 발생한다.|

- Response
```JSON
{
  "message": "Success",
  "crawlers": [
    {
      "crawler_id": "xvio31",
      "thumbnail_url": "http://steamcommunity-a.akamaihd.net/public/shared/images/header/globalheader_logo.png",
      "description": "스팀 할인 정보 크롤러",
      "title": "Steam "
    },
    {
      "crawler_id": "wf42i",
      "thumbnail_url": "http://wstatic.dcinside.com/main/main2011/dcmain/logo_swf/top_logo_160718.png",
      "description": "디시 힛겔 크롤러",
      "title": "DCinside "
    }]
}
```

###  3. Crawler Subscription List
- /req_subscription_list

|Data|Description|
|----|-----------|
|user_id|사용자 아이디|
|user_key|서버에서 발급받은 키, user_key없이 request를 날리면 <B>에러</B>가 발생한다.|

- Response
```JSON
{
  "message": "Success",
  "subscriptions": [
    "wf42i",
    "xvio31",
    ],
   "error": 0}
```

###  4. Subscribe Crawler
- /req_subscribe_crawler

|Data|Description|
|----|-----------|
|user_id|사용자 아이디|
|user_key|서버에서 발급받은 키, user_key없이 request를 날리면 <B>에러</B>가 발생한다.|
|crawler_id|구독하려는 크롤러 id|

- Response
```JSON
{
  "message": "Success",
  "error": 0
}
```

###  5. Unsubscribe Crawler
- /req_unsubscribe_crawler

|Data|Description|
|----|-----------|
|user_id|사용자 아이디|
|user_key|서버에서 발급받은 키, user_key없이 request를 날리면 <B>에러</B>가 발생한다.|
|crawler_id|구독하고있는 크롤러 id|

- Response
```JSON
{
  "message": "Success",
  "error": 0
}
```

###  6. Register Push Token
- /register_push_token

|Data|Description|
|----|-----------|
|user_id|사용자 아이디|
|user_key|서버에서 발급받은 키, user_key없이 request를 날리면 <B>에러</B>가 발생한다.|
|token|firebase cloud message token|

- Response
```JSON
{
  "message": "Success",
  "error": 0
}
```

###  7. Request Push
- /req_push
웹에서 요청하면 Push 토큰(FCM Device ID)를 등록한 사용자에게 Push 메시지를 보낸다.

|Data|Description|
|----|-----------|
|title|Push 타이틀|
|message|Push 메시지|

- Response
```JSON
{
  "message": "Success",
  "error": 0
}
```
