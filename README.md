# TCP Connection Simulator

-------
## Usage

-------
argument 4 = 1 for activating metadata sending
argument 4 = 2 for activating multithreading
no 4th argument for normal run

## Example usage:

-------
### Run normally
Server side:
```bash
./run_sender.sh 192.168.43.200,192.168.43.201 1337 ./.github/tests/in/1mb.medium.txt
```
Client side:
```bash
./run_receiver.sh 1337
```

### Run with metadata activated
Server side:
```bash
./run_sender.sh 192.168.43.200,192.168.43.201 1337 ./.github/tests/in/1mb.medium.txt 1
```
Client side:
```bash
./run_receiver.sh 1337
```

### Run with multithreading activated
Server side:
```bash
./run_sender.sh 192.168.43.200,192.168.43.201 1337 ./.github/tests/in/1mb.medium.txt 2
```
Client side:
```bash
./run_receiver.sh 1337
```