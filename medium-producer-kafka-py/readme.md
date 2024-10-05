
#### Reading using Kcat Json Topic
```shell
kcat -b localhost:9094 -t user_activity -J
```
Output:
```shell
(.venv) mateusoliveira@mateuss-MacBook-Pro medium-producer-kafka-py % kcat -b localhost:9094 -t user_activity -J
% Auto-selecting Consumer mode (use -P or -C to override)
{"topic":"user_activity","partition":0,"offset":0,"tstype":"create","ts":1727977685354,"broker":0,"key":"1","payload":"{\"id\": 1, \"name\": \"Alice\", \"age\": 30, \"created_at\": \"2024-10-03T14:48:05.333137\", \"event\": \"login\"}"}
{"topic":"user_activity","partition":0,"offset":1,"tstype":"create","ts":1727977685354,"broker":0,"key":"2","payload":"{\"id\": 2, \"name\": \"Bob\", \"age\": 25, \"created_at\": \"2024-10-03T14:48:05.333143\", \"event\": \"logout\"}"}
{"topic":"user_activity","partition":0,"offset":2,"tstype":"create","ts":1727977685354,"broker":0,"key":"3","payload":"{\"id\": 3, \"name\": \"Charlie\", \"age\": 35, \"created_at\": \"2024-10-03T14:48:05.333143\", \"event\": \"purchase\", \"amount\": 250.5}"}
% Reached end of topic user_activity [0] at offset 3
```
#### Reading using Kcat Avro Topic
```shell
kcat -b localhost:9094 -t user_activity_avro -s avro -r http://localhost:8081
```
Output:
```shell
(.venv) mateusoliveira@mateuss-MacBook-Pro medium-producer-kafka-py % kcat -b localhost:9094 -t user_activity_avro -s avro -r http://localhost:8081
% Auto-selecting Consumer mode (use -P or -C to override)
{"id": 2}{"id": 2, "name": "Bob", "age": 25, "created_at": "2024-10-03T15:20:22.205306", "event": "logout", "amount": null}
{"id": 1}{"id": 1, "name": "Alice", "age": 30, "created_at": "2024-10-03T15:20:22.205303", "event": "login", "amount": null}
{"id": 3}{"id": 3, "name": "Charlie", "age": 35, "created_at": "2024-10-03T15:20:22.205307", "event": "purchase", "amount": {"double": 250.5}}
```