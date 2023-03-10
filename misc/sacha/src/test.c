#include <openssl/rand.h>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include "../include/aes.h"
#include "../include/sha256.h"

struct Sha_256 sha_256;

void testReEncrypt()
{
    uint64_t size = 1 << 20;
    uint64_t elemsize = 128; // in blocks 62 * 128 bits = 1KB

    uint128_t *seeds = malloc(sizeof(uint128_t) * size);
    RAND_bytes((uint8_t *)seeds, sizeof(uint128_t) * size);

    float totalTime = 0;
    clock_t start = clock();
    uint64_t i;
    for (i = 0; i < size; i++)
    {
        // hash to get new key
        uint8_t hash[32];
        sha_256_init(&sha_256, hash);
        sha_256_write(&sha_256, (uint8_t *)&seeds[i], sizeof(uint128_t));
        sha_256_close(&sha_256);

        // key AES with the new key
        struct AES *aes = initAES((uint8_t *)&hash);
    }

    clock_t end = clock();
    float ms = (float)(end - start) / (CLOCKS_PER_SEC / 1000);
    totalTime += ms;
    printf("Re-keying AES took %f ms\n", ms);

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

    printf("Done filling database with random bytes\n");

    start = clock();
    reencrypt(aes, size, elemsize, database, output);
    end = clock();
    ms = (float)(end - start) / (CLOCKS_PER_SEC / 1000);
    totalTime += ms;
    printf("Re-encryption took %f ms\n", ms);

    uint64_t dbSizeBits = size * elemsize * 128;
    uint64_t bitsInMB = 8 * 1000000;
    uint64_t dbSizeMB = dbSizeBits / bitsInMB;
    printf("Re-encryption MB/s %f\n", dbSizeMB / (totalTime / 1000.0));

    free(database);
    free(output);
    destroyAES(aes);
}

int main(int argc, char **argv)
{

    int testTrials = 20;

    printf("******************************************\n");
    printf("Testing\n");
    testReEncrypt();
    printf("******************************************\n");
    printf("DONE\n");
    printf("******************************************\n\n");
}