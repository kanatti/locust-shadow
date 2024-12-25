# locust-shadow

How to run:


```
❯ uv run --package locust-shadow ./packages/locust-shadow/main.py ./dev/test-config.yaml
[2024-12-25 01:32:37,205] f4d4889b88f5/INFO/root: Loaded 2 minute batches.
[2024-12-25 01:32:37,205] f4d4889b88f5/INFO/root: Total shadow run duration will be 120 seconds (2.00 minutes).
[2024-12-25 01:32:37,205] f4d4889b88f5/INFO/locust.runners: Ramping to 1 users at a rate of 1.00 per second
[2024-12-25 01:32:37,205] f4d4889b88f5/INFO/locust.runners: All users spawned: {"DynamicMinuteBatchUser": 1} (1 total users)
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /echo?data=%7B%22colors%22%3A%5B%22red%22%2C%22green%22%2C%22blue%22%5D%7D         1     0(0.00%) |      2       2       2      2 |    0.00        0.00
GET      /echo?data=%7B%22message%22%3A%22Hello%2C+World%21%22%7D                           1     0(0.00%) |      6       6       6      6 |    0.00        0.00
GET      /echo?data=%7B%22name%22%3A%22John+Doe%22%2C%22age%22%3A30%7D                      1     0(0.00%) |      7       7       7      7 |    0.00        0.00
GET      /echo?data=%7B%22status%22%3A%22active%22%2C%22count%22%3A42%7D                    1     0(0.00%) |      5       5       5      5 |    0.00        0.00
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         4     0(0.00%) |      5       2       7      5 |    0.00        0.00

Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /echo?data=%7B%22colors%22%3A%5B%22red%22%2C%22green%22%2C%22blue%22%5D%7D         2     0(0.00%) |      3       2       5      2 |    0.00        0.00
GET      /echo?data=%7B%22error%22%3Anull%2C%22success%22%3Atrue%7D                         1     0(0.00%) |      7       7       7      7 |    0.00        0.00
GET      /echo?data=%7B%22message%22%3A%22Hello%2C+World%21%22%7D                           2     0(0.00%) |      6       5       6      6 |    1.00        0.00
GET      /echo?data=%7B%22name%22%3A%22John+Doe%22%2C%22age%22%3A30%7D                      2     0(0.00%) |      6       6       7      6 |    1.00        0.00
GET      /echo?data=%7B%22status%22%3A%22active%22%2C%22count%22%3A42%7D                    1     0(0.00%) |      5       5       5      5 |    0.00        0.00
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         8     0(0.00%) |      5       2       7      6 |    2.00        0.00

... <LOAD CHANGES DYNAMICALLY OVER TIME>

Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /echo?data=%7B%22colors%22%3A%5B%22red%22%2C%22green%22%2C%22blue%22%5D%7D        24     0(0.00%) |      4       1       7      4 |    0.00        0.00
GET      /echo?data=%7B%22error%22%3Anull%2C%22success%22%3Atrue%7D                        24     0(0.00%) |      4       2       8      4 |    0.00        0.00
GET      /echo?data=%7B%22message%22%3A%22Hello%2C+World%21%22%7D                          25     0(0.00%) |      4       1       9      4 |    0.00        0.00
GET      /echo?data=%7B%22name%22%3A%22John+Doe%22%2C%22age%22%3A30%7D                     24     0(0.00%) |      4       1       8      4 |    0.00        0.00
GET      /echo?data=%7B%22status%22%3A%22active%22%2C%22count%22%3A42%7D                   24     0(0.00%) |      4       2       7      5 |    0.00        0.00
GET      /echo?info=%7B%22colors%22%3A%5B%22red%22%2C%22green%22%2C%22blue%22%5D%7D        47  47(100.00%) |      4       1      26      3 |    0.80        0.80
GET      /echo?info=%7B%22error%22%3Anull%2C%22success%22%3Atrue%7D                        46  46(100.00%) |      4       1      15      3 |    0.80        0.80
GET      /echo?info=%7B%22message%22%3A%22Hello%2C+World%21%22%7D                          46  46(100.00%) |      4       1      12      3 |    0.80        0.80
GET      /echo?info=%7B%22name%22%3A%22John+Doe%22%2C%22age%22%3A30%7D                     47  47(100.00%) |      4       1      25      3 |    0.80        0.80
GET      /echo?info=%7B%22status%22%3A%22active%22%2C%22count%22%3A42%7D                   47  47(100.00%) |      3       1       8      3 |    0.80        0.80
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                       354  233(65.82%) |      4       1      26      4 |    4.00        4.00
```