TARGET = test
CFLAGS = -O3 -fpic
LDFLAGS = -lcrypto -lssl -lm

$(TARGET): test.o libpir.a
	gcc $^ -o $@ $(LDFLAGS)

test.so: test.o libpir.a
	gcc -shared -o $@ $^ $(LDFLAGS)
	make clean

test.o: test.c ../include/aes.h
	gcc $(CFLAGS) -c $< -o $@ $(LDFLAGS)

libpir.a: aes.o sha256.o
	ar rcs $@ $^

aes.o: aes.c ../include/aes.h 
	gcc $(CFLAGS) -c -o $@ $< $(LDFLAGS)

sha256.o: sha256.c ../include/sha256.h
	gcc $(CFLAGS) -c -o $@ $< 
clean:
	rm -f *.o *.a $(TARGET)
