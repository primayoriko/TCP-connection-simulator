#!/bin/bash

# Panggil program anda untuk mode siap mengirim file
# $1 berisi address receiver (akan diisi oleh autograder)
# $2 berisi port receiver (akan diisi oleh autograder)
# $3 berisi path file yang akan dikirim (akan diisi oleh autograder)
# Contoh: echo -e "$1\n$2\n$3" | python3 sender.py
# echo "Sender"

# python3 sender.py $1 $2 $3
if [ $# -eq 4 ]
then
  if [ $4 == "2" ]
  then
    echo "Starting multithreading mode!"
    python3 sender_multithread.py $1 $2 $3
  else
    echo "Starting metadata mode!"
    python3 sender.py $1 $2 $3 $4
  fi
else
  echo "Starting normal mode!"
  python3 sender.py $1 $2 $3
fi
# python3 sender_multithread.py $1 $2 $3