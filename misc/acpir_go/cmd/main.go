package main

import (
	"crypto/elliptic"
	"crypto/rand"
	"fmt"
	"math/big"
	"time"

	"../elgamal"
)

var NUM_TRIALS = 1000

func main() {
	pk, _ := elgamal.KeyGen(elliptic.P256(), 100)

	db := make(elgamal.Ciphertext, NUM_TRIALS)
	plainIn := make(elgamal.Plaintext, NUM_TRIALS)
	for i := 0; i < NUM_TRIALS; i++ {
		msg := rand.Int63n(7 * i)
		plainIn[i] = elgamal.NewPlaintext(big.NewInt(int64(msg)))
	}

	start := time.Now()
	for i := 0; i < NUM_TRIALS; i++ {
		db[i] = pk.Encrypt(plainIn)
	}

	totalTimeMS := time.Since(start)

	fmt.Println(totalTimeMS)

	throughputMBps := 0.000256 / (totalTimeMS / 1000) // 0.000256 is 256 B in MB
	fmt.Printf("Throughput (MB/s) = %v", throughputMBps)
}
