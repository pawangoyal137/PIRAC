#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

typedef unsigned __int128 uint128_t;

uint128_t *encryptDatabase(uint128_t *database, uint128_t seed, uint64_t size, uint64_t elemsize);
