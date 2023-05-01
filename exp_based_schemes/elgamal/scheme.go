package elgamal

import (
	"crypto/rand"
	"math/big"

	"github.com/pawangoyal137/PIRAC/exp_based_schemes/ec"
)

type Ciphertext struct {
	C0 *ec.Point // g^mh^r
	C1 *ec.Point // g^r
}

type Plaintext struct {
	M *big.Int
}

func NewPlaintext(m *big.Int) *Plaintext {
	return &Plaintext{m}
}

func (pk *PublicKey) Encrypt(m *Plaintext) *Ciphertext {

	_, rnd, err := ec.RandomCurveScalar(pk.Pk.Curve, rand.Reader)
	if err != nil {
		panic(err)
	}

	return pk.EncryptWithR(m, rnd)
}

func (pk *PublicKey) EncryptWithR(m *Plaintext, rnd *big.Int) *Ciphertext {

	C0 := ec.PointScalarMult(pk.Curve, pk.Pk, rnd)
	C1 := ec.BaseScalarMult(pk.Curve, rnd)

	if m.M.Cmp(big.NewInt(0)) != 0 {
		B := ec.BaseScalarMult(pk.Curve, m.M)
		C0 = ec.PointAdd(pk.Curve, B, C0)
	}

	return &Ciphertext{C0: C0, C1: C1}
}

func (sk *SecretKey) Decrypt(c *Ciphertext) *Plaintext {

	d := ec.PointScalarMult(sk.Pk.Curve, c.C1, sk.Sk)

	if ec.PointsEqual(d, c.C0) {
		// encryption of zero
		return &Plaintext{M: big.NewInt(0)}
	}

	d = ec.PointInverse(sk.Pk.Curve, d)
	gm := ec.PointAdd(sk.Pk.Curve, c.C0, d)

	m := big.NewInt(1)

	// (optional for large message space):
	// use more clever DL algorithm (e.g., baby-step-giant-step)
	for i := 1; i < sk.Pk.MsgBound; i++ {
		base := ec.BaseScalarMult(sk.Pk.Curve, m)

		if ec.PointsEqual(base, gm) {
			return &Plaintext{M: m}
		}

		if i+1 == sk.Pk.MsgBound {
			panic("could not decrypt; outside of range")
		}

		m.Add(m, big.NewInt(1))
	}

	return &Plaintext{}
}

func (pk *PublicKey) Add(a, b *Ciphertext) *Ciphertext {

	res0 := ec.PointAdd(pk.Curve, a.C0, b.C0)
	res1 := ec.PointAdd(pk.Curve, a.C1, b.C1)
	return &Ciphertext{C0: res0, C1: res1}
}

func (pk *PublicKey) ScalarMult(c *Ciphertext, scalar *big.Int) *Ciphertext {

	res0 := ec.PointScalarMult(pk.Curve, c.C0, scalar)
	res1 := ec.PointScalarMult(pk.Curve, c.C1, scalar)
	return &Ciphertext{C0: res0, C1: res1}
}
