CC = g++
CFLAGS = -Wall
SRC = ./src
TARGETS = bppg.out
SOURCES = $(wildcard $(SRC)/*.cpp) $(wildcard $(SRC)/DataFrame/*.cpp)

all:
	$(CC) $(SOURCES) $(HEADERS) -o $(TARGETS)

clean:
	rm -r $(TARGETS)

