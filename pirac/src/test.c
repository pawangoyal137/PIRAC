#include <openssl/rand.h>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include "../include/aes.h"

float runKeyRefresh(size_t num_keys)
{
    static EVP_CIPHER_CTX *prf_ctx;
    if (!prf_ctx)
    {
        if (!(prf_ctx = EVP_CIPHER_CTX_new()))
            printf("errors ocurred when generating PRF context\n");
    }

    uint128_t *old_seeds = malloc(sizeof(uint128_t) * num_keys);
    uint128_t *new_seeds = malloc(sizeof(uint128_t) * num_keys);

    if (!RAND_bytes((uint8_t *)&old_seeds[0], sizeof(uint128_t) * num_keys))
        printf("failed to seed randomness\n");

    clock_t start = clock();

    int status = 0;
    int len = 0;
    uint8_t epoch[16]; // TODO: set desired epoch number; currently zero for testing

    for (int i = 0; i < num_keys; i++)
    {
        // okay to use ECB mode here because we're using it as a PRF
        status = EVP_EncryptInit_ex(prf_ctx, EVP_aes_128_ecb(), NULL, (uint8_t *)&old_seeds[i], NULL);

        // DEBUG
        // if (status != 1)
        //     printf("errors ocurred when refreshing key with PRF\n");

        // apply PRF to epoch number to get new key
        status = EVP_EncryptUpdate(prf_ctx, (uint8_t *)&new_seeds[i], &len, &epoch[0], 16);

        // DEBUG
        // if (status != 1)
        //     printf("failed to generate new key with PRF\n");
    }

    // key AES with the new keys
    struct AES *new_keys = initAESKeys(new_seeds, num_keys);

    free(old_seeds);
    free(new_seeds);
    free(new_keys);

    clock_t end = clock();
    float totalTime = (float)(end - start) / (CLOCKS_PER_SEC / 1000);

    return totalTime;
}

float runReEncryption(uint64_t db_size, uint64_t elem_size)
{
    uint128_t *seeds = malloc(sizeof(uint128_t) * db_size);
    RAND_bytes((uint8_t *)seeds, sizeof(uint128_t) * db_size);

    float total_time = 0;
    struct AES *aes_keys = initAESKeys(seeds, db_size);

    uint128_t *database = malloc(sizeof(uint128_t) * db_size * elem_size);
    uint128_t *output = malloc(sizeof(uint128_t) * db_size * elem_size);

    if (database == NULL || output == NULL)
    {
        printf("failed to allocate space");
        exit(0);
    }

    RAND_bytes((uint8_t *)database, sizeof(uint128_t) * db_size * elem_size);

    clock_t start = clock();
    reEncrypt(aes_keys, db_size, elem_size, database, output);
    clock_t end = clock();
    total_time = (float)(end - start) / (CLOCKS_PER_SEC / 1000);

    free(database);
    free(output);
    free(seeds);

    destroyAESKeys(aes_keys, db_size);

    return total_time;
}

int main(int argc, char **argv)
{

    uint64_t db_size = 1 << 20;
    uint64_t elem_block_size = 2;

    printf("******************************************\n");
    printf("Testing with n=%llu and l=%llu (aes blocks)\n", db_size, elem_block_size);
    printf("******************************************\n");
    float totalTime = runKeyRefresh(db_size);
    printf("Key refresh took %f ms\n", totalTime);

    printf("******************************************\n");
    totalTime = runReEncryption(db_size, elem_block_size);
    printf("Re-encryption took %f ms\n", totalTime);
    printf("******************************************\n");

    printf("DONE\n");
}