OBJS = serialComm.o
CC = g++
CFLAGS = -Wall -c -mwindows $(DEBUG)
LFLAGS = -Wall $(DEBUG)

pressureRead : $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) -o pressureRead

clean:
	\rm *.o *~ pressureRead

tar:
	tar cfv pressureRead.tar serialComm.c