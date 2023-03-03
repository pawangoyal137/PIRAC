TARGET = test
CFLAGS = -O3
LDFLAGS = -L/usr/local/Cellar//openssl@3/3.0.8/lib/ -lcrypto -lssl -lm

$(TARGET): test.o libpir.a
	gcc $^ -o $@ $(LDFLAGS)

test.so: test.o libpir.a
	gcc -shared -o $@ $^ $(LDFLAGS)
	make clean

test.o: test.c ../include/aes.h
	gcc $(CFLAGS) -fpic -c $< -o $@ $(LDFLAGS)

libpir.a: aes.o sha256.o
	ar rcs $@ $^

aes.o: aes.c ../include/aes.h 
	gcc $(CFLAGS) -c -o $@ $< $(LDFLAGS)

clean:
	rm -f *.o *.a $(TARGET)