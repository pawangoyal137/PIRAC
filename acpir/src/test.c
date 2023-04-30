#include <openssl/rand.h>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include "../include/aes.h"

float runKeyRefresh(uint64_t numRefreshOps)
{
    static EVP_CIPHER_CTX *prfCtx;
    if (!prfCtx)
    {
        if (!(prfCtx = EVP_CIPHER_CTX_new()))
            printf("errors ocurred when generating context\n");
    }

    uint8_t *oldKey = (uint8_t *)malloc(16);
    uint8_t *newKey = (uint8_t *)malloc(16);
    if (!RAND_bytes(oldKey, 16))
        printf("failed to seed randomness\n");

    clock_t start = clock();

    for (int i = 0; i < numRefreshOps; i++)
    {
        if (1 != EVP_EncryptInit_ex(prfCtx, EVP_aes_128_ecb(), NULL, oldKey, NULL))
            printf("errors ocurred when generating context\n");
        EVP_CIPHER_CTX_set_padding(prfCtx, 0);

        uint8_t epoch[16]; // TODO: set desired epoch number; currently zero

        // apply PRF to epoch to get new key
        int len = 0;
        if (1 != EVP_EncryptUpdate(prfCtx, (uint8_t *)newKey, &len, (uint8_t *)&epoch, 16))
            printf("failed to generate new key\n");

        // key AES with the new key
        initAES((uint8_t *)newKey);

        *oldKey = *newKey;
    }

    free(oldKey);
    free(newKey);

    clock_t end = clock();
    float totalTime = (float)(end - start) / (CLOCKS_PER_SEC / 1000);
    // printf("Key refresh took %f ms\n", totalTime);
    return totalTime;
}

float runReEncryption(uint64_t size, uint64_t elemsize)
{
    uint128_t *seeds = malloc(sizeof(uint128_t) * 1);
    RAND_bytes((uint8_t *)seeds, sizeof(uint128_t) * 1);

    float totalTime = 0;
    uint128_t seed = seeds[0];
    free(seeds);
    struct AES *aes = initAES((uint8_t *)&seed);

    uint128_t *database = malloc(sizeof(uint128_t) * size * elemsize);
    uint128_t *output = malloc(sizeof(uint128_t) * size * elemsize);

    if (database == NULL || output == NULL)
    {
        printf("failed to allocate space");
        exit(0);
    }
    RAND_bytes((uint8_t *)database, sizeof(uint128_t) * size * elemsize);

    clock_t start = clock();
    reencrypt(aes, size, elemsize, database, output);
    clock_t end = clock();
    totalTime = (float)(end - start) / (CLOCKS_PER_SEC / 1000);
    // printf("Re-encryption took %f ms\n", totalTime);

    free(database);
    free(output);
    destroyAES(aes);

    return totalTime;
}

int main(int argc, char **argv)
{

    uint64_t size = 1<<16;
    uint64_t elemsize_128bits = 2;


    printf("******************************************\n");
    printf("Testing\n");
    runKeyRefresh(size),
    printf("******************************************\n");
    runReEncryption(size, elemsize_128bits);
    printf("******************************************\n\n");
    printf("DONE\n");
}