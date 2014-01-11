all:	test

OBJ = sunyard.o test.o
test:	$(OBJ)
		cc -o test $(OBJ) -lc 
		rm *.o

test.o:	test.c
		cc -c test.c

sunyard.o:	sunyard.c sunyard.h
		cc -c sunyard.c 
