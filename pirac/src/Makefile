TARGET = test
CFLAGS = -O3 -fpic
LDFLAGS = -march=native -lcrypto -lssl -lm -maes -ffast-math

$(TARGET): test.o libpir.a
	gcc $^ -o $@ $(LDFLAGS)

test.so: test.o libpir.a
	gcc -shared -o $@ $^ $(LDFLAGS)
	make clean

test.o: test.c ../include/aes.h
	gcc $(CFLAGS) -c $< -o $@ $(LDFLAGS)

libpir.a: aes.o 
	ar rcs $@ $^

aes.o: aes.c ../include/aes.h 
	gcc $(CFLAGS) -c -o $@ $< $(LDFLAGS)

clean:
	rm -f *.o *.a $(TARGET)
