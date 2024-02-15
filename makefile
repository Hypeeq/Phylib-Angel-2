CC = clang
CFLAGS = -std=c99 -Wall -pedantic
LDFLAGS = -L. -lphylib -lm
PYTHON_INCLUDE = /usr/include/python3.11/
PYTHON_LIB = /usr/lib/python3.11/

all: libphylib.so _phylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fpic -c $< -o $@

libphylib.so: phylib.o
	$(CC) -shared -o $@ $<

A1test1: A1test1.c phylib.h libphylib.so
	$(CC) $(CFLAGS) $< $(LDFLAGS) -o $@

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) -shared phylib_wrap.o -L$(PYTHON_LIB) -lpython3.11 -lphylib -o $@

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c $< -I$(PYTHON_INCLUDE) -fPIC -o $@

phylib_wrap.c: phylib.i
	swig -python $<

clean:
	rm -f *.o *.so A1test1 _phylib.so
	export LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:`pwd`
	-rm -f phylib_wrap.c
	-rm -f phylib_wrap.o
	clang -Wall -pedantic -std=c99 -fPIC -c phylib.c -o phylib.o
	clang -shared -o libphylib.so phylib.o -lm
	clang -Wall -pedantic -std=c99 -c phylib_wrap.c -I$(PYTHON_INCLUDE) -fPIC -o phylib_wrap.o
	clang -Wall -pedantic -std=c99 -shared phylib_wrap.o -L$(PYTHON_LIB) -lpython3.11 -lphylib -o _phylib.so
