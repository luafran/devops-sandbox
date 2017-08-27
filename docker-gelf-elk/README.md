### Kibana Dashboard

http://localhost:5601

user: elastic
passwd: changeme

### Test logging using one-shot container

```shell
docker run --log-driver gelf --log-opt gelf-address=udp://127.0.0.1:12201 --rm alpine echo hello world
```

### References
[docker-elk examples](https://github.com/deviantony/docker-elk/tree/x-pack)
[elastic x-pack reference](https://www.elastic.co/guide/en/x-pack/current/xpack-introduction.html)
