package paillier

import (
    "math/big"
	"testing"
	"time"
	"fmt"
	"math"
)

var NUMITERS int = 1000

func BenchmarkMultiplyMod(b *testing.B) {
    bits := 3072
    x := generateRandomNumber(bits)
    y := generateRandomNumber(bits)
    z := generateCompositeNumber(bits)

	b.ResetTimer()
    for n := 0; n < b.N; n++ {
        new(big.Int).Mod(new(big.Int).Mul(x, y), z)
    }
}

// benchmark where a new triplet is calculated for each iteration
func BenchmarkMultiplyModDifPrimes(b *testing.B) {
    bits := 3072

	numIter := int(math.Max(float64(NUMITERS), float64(b.N)))
	var totalTime time.Duration
    for i := 0; i < numIter; i++ {
		x := generateRandomNumber(bits)
		y := generateRandomNumber(bits)
		z := generateCompositeNumber(bits)

        start := time.Now()
        new(big.Int).Mod(new(big.Int).Mul(x, y), z)
        totalTime += time.Since(start)
    }

    // calculate and print the average time taken per iteration
    averageTime := totalTime / time.Duration(numIter)
    fmt.Printf("Average time for multiplication per iteration over %d loops: %v\n", numIter, averageTime)
}

func BenchmarkExponentMod(b *testing.B) {
    bits := 3072
    x := generateRandomNumber(bits)
    y := generateRandomNumber(bits)
    z := generateCompositeNumber(bits)

	b.ResetTimer()
    for n := 0; n < b.N; n++ {
        new(big.Int).Exp(x, y, z)
    }
}

// benchmark where a new triplet is calculated for each iteration
func BenchmarkExponentModDifPrimes(b *testing.B) {
    bits := 3072

	numIter := int(math.Max(float64(NUMITERS), float64(b.N)))
	var totalTime time.Duration
    for i := 0; i < numIter; i++ {
		x := generateRandomNumber(bits)
		y := generateRandomNumber(bits)
		z := generateCompositeNumber(bits)

        start := time.Now()
        new(big.Int).Exp(x, y, z)
        totalTime += time.Since(start)
    }

    // calculate and print the average time taken per iteration
    averageTime := totalTime / time.Duration(numIter)
    fmt.Printf("Average time for exponentiation per iteration over %d loops: %v\n", numIter, averageTime)
}

func BenchmarkPaillier(b *testing.B) {
    bits := 3072
    x := generateRandomNumber(bits)
    y := generateRandomNumber(bits)
    z := generateCompositeNumber(bits)

	b.ResetTimer()
    for n := 0; n < b.N; n++ {
        new(big.Int).Exp(x, y, z)
        new(big.Int).Mod(new(big.Int).Mul(x, y), z)
    }
}

func BenchmarkPaillierDifPrimes(b *testing.B) {
    bits := 3072

	numIter := int(math.Max(float64(NUMITERS), float64(b.N)))
	var totalTime time.Duration
    for i := 0; i < numIter; i++ {
		x := generateRandomNumber(bits)
		y := generateRandomNumber(bits)
		z := generateCompositeNumber(bits)

        start := time.Now()
        new(big.Int).Exp(x, y, z)
        new(big.Int).Mod(new(big.Int).Mul(x, y), z)
        totalTime += time.Since(start)
    }

    // calculate and print the average time taken per iteration
    averageTime := totalTime / time.Duration(numIter)
    fmt.Printf("Average time for paillier per iteration over %d loops: %v\n", numIter, averageTime)
}