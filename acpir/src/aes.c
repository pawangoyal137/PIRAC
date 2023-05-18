#include "../include/aes.h"
#include <stdint.h>

struct AES *initAES(uint8_t *seed)
{
    EVP_CIPHER_CTX *ctx = malloc(sizeof(EVP_CIPHER_CTX *));
    struct AES *aes = malloc(sizeof(struct AES));

    if (!(ctx = EVP_CIPHER_CTX_new()))
        printf("aes context error\n");

    int status = EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, (uint8_t *)seed, NULL);
    if (status != 1)
        printf("aes randomness init error\n");

    EVP_CIPHER_CTX_set_padding(ctx, 0);

    aes->ctx = ctx;
    return aes;
}

void reencrypt(struct AES *aes, uint64_t size, uint64_t elemsize, uint128_t *input, uint128_t *output)
{
    uint64_t i;
    for (i = 0; i < size * elemsize; i += elemsize)
    {
        int len = 0;
        int status = EVP_EncryptUpdate(aes->ctx, (uint8_t *)&output[i], &len, (uint8_t *)&input[i], sizeof(uint128_t) * elemsize);
        if (status != 1)
            printf("errors occurred when encrypting\n");
    }
}

void destroyAES(struct AES *aes)
{
    EVP_CIPHER_CTX_free(aes->ctx);
    free(aes);
}
