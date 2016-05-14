.PHONY: all clean

all: bin/drwc

bin/drwc: drwc.c
	gcc -Wall -std=c99 $^ -o $@

clean:
	rm -f bin/drwc
