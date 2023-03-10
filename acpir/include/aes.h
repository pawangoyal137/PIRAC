#ifndef _MMO
#define _MMO

#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

typedef __int128 int128_t;
typedef unsigned __int128 uint128_t;

struct AES
{
   EVP_CIPHER_CTX *ctx;
};
typedef struct aes AES;

// cipher context
extern struct AES *initAES(uint8_t *seed);
extern void destroyAES(struct AES *aes);

extern void reencrypt(struct AES *aes, uint64_t size, uint64_t elemsize, uint128_t *input, uint128_t *output);

#endif
