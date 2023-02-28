#include <openssl/rand.h>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include "../include/encryption.h"
#include "../include/aes.h"
#include "../include/sha256.h"

struct Sha_256 sha_256;

uint64_t *encryptDatabase(uint64_t *database, uint64_t seed, uint64_t size, uint64_t elemsize){
    struct AES *aes = initAES((uint8_t *)&seed);
    uint64_t *encrpytedDB = malloc(sizeof(uint64_t) * size * elemsize);
    if (encrpytedDB == NULL)
    {
        printf("failed to allocate space");
        exit(0);
    }
    if (sizeof(*encrpytedDB) != sizeof(*database))
    {
        printf("Different size of input and output database");
        exit(0);
    }
    reencrypt(aes, size, elemsize, database, encrpytedDB);

    return encrpytedDB;
}