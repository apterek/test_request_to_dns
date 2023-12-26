# test_request_to_dns
### Run the script as root because you need to access system sockets

### First of all, install the necessary libraries
```commandline
   pip3 install -r requirements.txt
```

Example run script (10,000 domains will be generated and run in 10 threads):
```commandline
  python3 requester.py -d 10000 -t 10
```
```commandline
The -d flag is used to set the number of generated domain names,
in fact this affects the duration of the script
```
```commandline
The -е flag is used to set the number of threads
that is it affects the number of requests per second
```

### P.S. 
#### For better performance use python 3.11 or higher