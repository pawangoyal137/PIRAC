TARGET = test
CFLAGS = -O3
LDFLAGS = -lcrypto -lssl -lm

$(TARGET): test.o libpir.a
	gcc $^ -o $@ $(LDFLAGS)

test.o: test.c ../include/aes.h
	gcc $(CFLAGS) -c $< -o $@ $(LDFLAGS)

libpir.a: aes.o sha256.o
	ar rcs $@ $^

aes.o: aes.c ../include/aes.h 
	gcc $(CFLAGS) -c -o $@ $< $(LDFLAGS)

clean:
	rm -f *.o *.a $(TARGET)