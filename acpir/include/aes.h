#ifndef _MMO
#define _MMO

#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

struct AES
{
   EVP_CIPHER_CTX *ctx;
};
typedef struct aes AES;

// cipher context
extern struct AES *initAES(uint8_t *seed);
extern void destroyAES(struct AES *aes);

extern void reencrypt(struct AES *aes, uint64_t size, uint64_t elemsize, uint64_t *input, uint64_t *output);

#endif
