### how to run

```
usage: main.py [-h] [--init] [--debug] [--stage STAGE] [--token TOKEN] studentId

positional arguments:
  studentId      Your student ID

optional arguments:
  -h, --help     show this help message and exit
  --init         Retrieves the first task description
  --debug        better logging
  --stage STAGE  stage to continue on
  --token TOKEN  token for stage
```

To solve all challenges automatically, just run `python main.py <studentId>`.

If you already have a valid token from a previous stage / task (e.g. in case not all stages are implemented in main.py and the program stopped before completing all stages) and want to continue without re-running old tasks, use the `--stage` and `--token` options

