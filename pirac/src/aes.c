#include "../include/aes.h"
#include <stdint.h>

struct AES *initAESKeys(uint128_t *seeds, int num_keys)
{
    struct AES *keys = malloc(sizeof(struct AES) * num_keys);
    int status = 0;

    for (int i = 0; i < num_keys; i++)
    {
        EVP_CIPHER_CTX *ctx = malloc(sizeof(EVP_CIPHER_CTX *));

        if (!(ctx = EVP_CIPHER_CTX_new()))
            printf("error when initializing aes context\n");

        status = EVP_EncryptInit_ex(
            ctx, EVP_aes_128_ctr(), NULL, (uint8_t *)&seeds[i], NULL);

        if (status != 1)
            printf("error when initializing aes key\n");

        EVP_CIPHER_CTX_set_padding(ctx, 0);

        keys[i].ctx = ctx;
    }

    return keys;
}

void reEncrypt(
    struct AES *aes_keys,
    uint64_t db_size,
    uint64_t elem_size,
    uint128_t *input,
    uint128_t *output)
{
    size_t i;
    size_t k;
    int len = 0;
    int status = 0;
    size_t num_blocks_total = db_size * elem_size;
    size_t num_blocks_per_enc = sizeof(uint128_t) * elem_size;

    for (i = 0; i < num_blocks_total; i += elem_size)
    {

        EVP_EncryptUpdate(
            aes_keys[k].ctx, (uint8_t *)&output[i],
            &len, (uint8_t *)&input[i], num_blocks_per_enc);

        // DEBUG
        // status = EVP_EncryptUpdate(
        //     aes_keys[k].ctx, (uint8_t *)&output[i],
        //     &len, (uint8_t *)&input[i],
        //     sizeof(uint128_t) * elem_size);

        // if (status != 1)
        //     printf("errors occurred when encrypting\n");

        k++;
    }
}

void destroyAESKeys(struct AES *aes_keys, int num_keys)
{
    for (int i = 0; i < num_keys; i++)
        EVP_CIPHER_CTX_free(aes_keys[i].ctx);

    free(aes_keys);
}
