package elgamal

import (
	"crypto/elliptic"
	crand "crypto/rand"
	"math/big"
	"math/rand"
	"testing"

	"exp_based_schemes/ec"
)

func TestEncryptDecrypt(t *testing.T) {
	for i := 0; i < 100; i++ {
		pk, sk := KeyGen(elliptic.P256(), 100)

		msg := rand.Int63n(100)

		plainIn := NewPlaintext(big.NewInt(int64(msg)))
		c := pk.Encrypt(plainIn)
		plainOut := sk.Decrypt(c)

		if plainOut.M.Cmp(plainIn.M) != 0 {
			t.Error("decryption failed")

		}
	}
}

func TestHomomorphicAdd(t *testing.T) {
	for i := 0; i < 100; i++ {
		pk, sk := KeyGen(elliptic.P256(), 200) // bound should be bigger than m1+m2

		msg1 := rand.Int63n(100)
		msg2 := rand.Int63n(100)

		plain1 := NewPlaintext(big.NewInt(int64(msg1)))
		plain2 := NewPlaintext(big.NewInt(int64(msg2)))

		c1 := pk.Encrypt(plain1)
		c2 := pk.Encrypt(plain2)
		c := pk.Add(c1, c2)

		plainOut := sk.Decrypt(c)

		expected := big.NewInt(msg1 + msg2)
		if plainOut.M.Cmp(expected) != 0 {
			t.Error("decryption failed")

		}
	}
}

func TestHomomorphicScalarMult(t *testing.T) {
	for i := 0; i < 100; i++ {
		pk, sk := KeyGen(elliptic.P256(), 1000) // bound should be bigger than m1+m2

		msg1 := rand.Int63n(100)
		scalar := rand.Int63n(9)

		plain := NewPlaintext(big.NewInt(int64(msg1)))
		c := pk.Encrypt(plain)
		c = pk.ScalarMult(c, big.NewInt(scalar))

		plainOut := sk.Decrypt(c)

		expected := big.NewInt(msg1 * scalar)
		if plainOut.M.Cmp(expected) != 0 {
			t.Error("decryption failed")

		}
	}
}

func BenchmarkExp(b *testing.B) {
	pk, _ := KeyGen(elliptic.P256(), 1000) // bound should be bigger than m1+m2

	msg1 := rand.Int63n(100)

	_, scalar, _ := ec.RandomCurveScalar(pk.Pk.Curve, crand.Reader)

	plain := NewPlaintext(big.NewInt(int64(msg1)))
	c := pk.Encrypt(plain)

	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		pk.ScalarMult(c, scalar)
	}
}
