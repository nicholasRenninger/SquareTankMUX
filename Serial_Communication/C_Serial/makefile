OBJS = serialComm.o
CC = i586-mingw32msvc-g++ 
DEBUG = -g
CFLAGS = -Wall -c -mwindows $(DEBUG)
LFLAGS = -Wall $(DEBUG)

pressureRead : $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) -o pressureRead

clean:
	\rm *.o *~ pressureRead

tar:
	tar cfv pressureRead.tar serialComm.c