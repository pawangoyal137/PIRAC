#ifndef _MMO
#define _MMO

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <openssl/evp.h>

typedef __int128 int128_t;
typedef unsigned __int128 uint128_t;

struct AES
{
   EVP_CIPHER_CTX *ctx;
};

typedef struct aes AES;

// cipher context
extern struct AES *initAESKeys(uint128_t *seed, int num_keys);
extern void destroyAESKeys(struct AES *aes, int num_keys);
extern void reEncrypt(struct AES *aes_keys, uint64_t db_size, uint64_t elem_size, uint128_t *input, uint128_t *output);

#endif
