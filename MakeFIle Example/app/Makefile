ifeq ($(OS),Windows_NT)
	uname_S := Windows
else
	uname_S := $(shell uname -s)
endif

ifeq ($(uname_S), Windows)
	target = app.exe
endif
ifeq ($(uname_S), Linux)
	target = app
endif
#ifeq ($(uname_S), .....) #See https://stackoverflow.com/a/27776822/938111
#    target = .....
#endif

%.o: %.c
	gcc  -c $< -I ../lib  -o $@
	# -c $<     => compile (-c) $< (first file after :) = main.c
	# -I ../lib => search headers (*.h) in directory ../lib
	# -o $@     => output file (-o) is $@ (target) = main.o

$(target): main.o
	gcc  $^  -L../lib  -lhello  -o $@
	# $^       => $^ (all files after the :) = main.o (here only one file)
	# -L../lib => look for libraries in directory ../lib
	# -lhello  => use shared library hello (libhello.so or hello.dll)
	# -o $@    => output file (-o) is $@ (target) = "app.exe" or "app"