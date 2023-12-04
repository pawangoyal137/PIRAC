package paillier

import (
    "math/big"
	"testing"
	"time"
	"fmt"
	"math"
)

var NUMITERS int = 1000
var BITS int = 2048

func BenchmarkMultiplyMod(b *testing.B) {
    x := generateRandomNumber(BITS)
    y := generateRandomNumber(BITS)
    z := generateCompositeNumber(BITS)

	b.ResetTimer()
    for n := 0; n < b.N; n++ {
        new(big.Int).Mod(new(big.Int).Mul(x, y), z)
    }
}

// benchmark where a new triplet is calculated for each iteration
func BenchmarkMultiplyModDifPrimes(b *testing.B) {
    numIter := int(math.Max(float64(NUMITERS), float64(b.N)))
	var totalTime time.Duration
    for i := 0; i < numIter; i++ {
		x := generateRandomNumber(BITS)
		y := generateRandomNumber(BITS)
		z := generateCompositeNumber(BITS)

        start := time.Now()
        new(big.Int).Mod(new(big.Int).Mul(x, y), z)
        totalTime += time.Since(start)
    }

    // calculate and print the average time taken per iteration
    averageTime := totalTime / time.Duration(numIter)
    fmt.Printf("Average time for multiplication per iteration over %d loops: %v\n", numIter, averageTime)
}

func BenchmarkExponentMod(b *testing.B) {
    x := generateRandomNumber(BITS)
    y := generateRandomNumber(BITS)
    z := generateCompositeNumber(BITS)

	b.ResetTimer()
    for n := 0; n < b.N; n++ {
        new(big.Int).Exp(x, y, z)
    }
}

// benchmark where a new triplet is calculated for each iteration
func BenchmarkExponentModDifPrimes(b *testing.B) {
    numIter := int(math.Max(float64(NUMITERS), float64(b.N)))
	var totalTime time.Duration
    for i := 0; i < numIter; i++ {
		x := generateRandomNumber(BITS)
		y := generateRandomNumber(BITS)
		z := generateCompositeNumber(BITS)

        start := time.Now()
        new(big.Int).Exp(x, y, z)
        totalTime += time.Since(start)
    }

    // calculate and print the average time taken per iteration
    averageTime := totalTime / time.Duration(numIter)
    fmt.Printf("Average time for exponentiation per iteration over %d loops: %v\n", numIter, averageTime)
}

func BenchmarkPaillier(b *testing.B) {    
    x := generateRandomNumber(BITS)
    y := generateRandomNumber(BITS)
    z := generateCompositeNumber(BITS)

	b.ResetTimer()
    for n := 0; n < b.N; n++ {
        new(big.Int).Exp(x, y, z)
        new(big.Int).Mod(new(big.Int).Mul(x, y), z)
    }
}

func BenchmarkPaillierDifPrimes(b *testing.B) {
	numIter := int(math.Max(float64(NUMITERS), float64(b.N)))
    var totalTime time.Duration
    var times []float64

    for i := 0; i < numIter; i++ {
		x := generateRandomNumber(BITS)
		y := generateRandomNumber(BITS)
		z := generateCompositeNumber(BITS)

        start := time.Now()
        new(big.Int).Exp(x, y, z)
        new(big.Int).Mod(new(big.Int).Mul(x, y), z)

        elapsed := time.Since(start)
        times = append(times, float64(elapsed.Microseconds()))
        totalTime += elapsed
    }

    averageTime := float64(totalTime.Milliseconds()) / float64(numIter) // in milli seconds

    // calculate standard deviation
	sumSquares := 0.0
	for _, elapsed := range times {
		diff := elapsed/1000 - averageTime
		sumSquares += diff * diff
    }
    stdDev := math.Sqrt(sumSquares / float64(numIter))
    
    // calculate tput and std in tput
    tput := (float64(BITS)/8)/(1000*float64(averageTime))
    fmt.Printf("Average time for paillier per iteration over %d loops: %v\n", numIter, averageTime)
    fmt.Printf("Average throughput for paillier: %f MB/s\n", tput)
    fmt.Printf("Standard Deviation in throughput for paillier: %f MB/s\n", tput*stdDev/averageTime)
}