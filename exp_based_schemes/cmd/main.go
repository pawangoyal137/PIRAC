package main

import (
	"crypto/elliptic"
	"fmt"
	"math/big"
	"math/rand"
	"time"

	"github.com/pawangoyal137/PIRAC/exp_based_schemes/elgamal"
)

var NUM_TRIALS = 1000

func main() {
	pk, _ := elgamal.KeyGen(elliptic.P256(), 100)

	db := make([]*elgamal.Ciphertext, NUM_TRIALS)
	plainIn := make([]*elgamal.Plaintext, NUM_TRIALS)
	for i := 0; i < NUM_TRIALS; i++ {
		msg := rand.Int63n(int64(100 + 7*i)) // create unique message
		plainIn[i] = elgamal.NewPlaintext(big.NewInt(int64(msg)))
	}

	start := time.Now()
	for i := 0; i < NUM_TRIALS; i++ {
		db[i] = pk.Encrypt(plainIn[i])
	}

	totalTimeMS := time.Since(start).Milliseconds()
	totalTimeS := float64(totalTimeMS) / 1000.0
	fmt.Println(totalTimeS)

	timePerCiphertextS := float64(totalTimeS) / float64(NUM_TRIALS)
	// 32 bytes in MB = float64(32/(1000000))
	throughputMBps := float64(32.0/(1000000)) / timePerCiphertextS
	fmt.Printf("Throughput (MB/s) = %v\n", throughputMBps)
}
