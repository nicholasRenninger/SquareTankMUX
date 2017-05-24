OBJS = serialComm.o
CC = g++
DEBUG = -g
CFLAGS = -Wall -c $(DEBUG)
LFLAGS = -Wall $(DEBUG)

pressureRead : $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) -o pressureRead

clean:
	\rm *.o *~ pressureRead

tar:
	tar cfv pressureRead.tar serialComm.c