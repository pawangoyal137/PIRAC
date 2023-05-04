package paillier

import (
    "crypto/rand"
    "math/big"
)

func generateRandomNumber(bits int) *big.Int {
    max := new(big.Int).Lsh(big.NewInt(1), uint(bits))
    n, err := rand.Int(rand.Reader, max)
    if err != nil {
        panic(err)
    }
    return n
}

func isComposite(n *big.Int) bool {
    return n.ProbablyPrime(20) == false
}

func generateCompositeNumber(bits int) *big.Int {
    for {
        n := generateRandomNumber(bits)
        if isComposite(n) {
            return n
        }
    }
}

