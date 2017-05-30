ifeq ($(OS),Windows_NT)
	uname_S := Windows
else
	uname_S := $(shell uname -s)
endif

ifeq ($(uname_S), Windows)
	target = hello.dll
endif
ifeq ($(uname_S), Linux)
	target = libhello.so
endif
#ifeq ($(uname_S), .....) #See https://stackoverflow.com/a/27776822/938111
#    target = .....
#endif

%.o: %.c
	gcc  -c $<  -fPIC  -o $@    
	# -c $<  => $< is first file after ':' => Compile hello.c
	# -fPIC  => Position-Independent Code (required for shared lib)
	# -o $@  => $@ is the target => Output file (-o) is hello.o

$(target): hello.o
	gcc  $^  -shared  -o $@
	# $^      => $^ expand to all prerequisites (after ':') => hello.o
	# -shared => Generate shared library
	# -o $@   => Output file (-o) is $@ (libhello.so or hello.dll)