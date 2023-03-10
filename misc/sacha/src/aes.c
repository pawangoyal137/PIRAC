// Implementation of the Matyas–Meyer–Oseas one-way compression function.
// See https://crypto.stackexchange.com/questions/56247/matyas-meyer-oseas-for-super-fast-single-block-hash-function
// and https://en.wikipedia.org/wiki/One-way_compression_function

#include "../include/aes.h"
#include <openssl/rand.h>
#include <stdint.h>
#include <time.h>
#include <math.h>

struct AES *initAES(uint8_t *seed)
{
    EVP_CIPHER_CTX *ctx = malloc(sizeof(EVP_CIPHER_CTX *));
    struct AES *aes = malloc(sizeof(struct AES));

    if (!(ctx = EVP_CIPHER_CTX_new()))
        printf("errors occured in creating context\n");

    if (1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, (uint8_t *)seed, NULL))
        printf("errors occurred in randomness init\n");

    EVP_CIPHER_CTX_set_padding(ctx, 0);

    aes->ctx = ctx;
    return aes;
}

void destroyAES(struct AES *aes)
{
    EVP_CIPHER_CTX_free(aes->ctx);
    free(aes);
}

void reencrypt(struct AES *aes, uint64_t size, uint64_t elemsize, uint128_t *input, uint128_t *output)
{
    uint64_t i;
    for (i = 0; i < size * elemsize; i += elemsize)
    {
        int len = 0;
        if (1 != EVP_EncryptUpdate(aes->ctx, (uint8_t *)&output[i], &len, (uint8_t *)&input[i], sizeof(uint128_t) * elemsize))
            printf("errors occurred when encrypting\n");
    }
}
