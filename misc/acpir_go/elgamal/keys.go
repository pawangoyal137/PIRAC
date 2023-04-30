package elgamal

import (
	"crypto/elliptic"
	crand "crypto/rand"
	"math/big"

	"../ec"
)

type PublicKey struct {
	Pk       *ec.Point
	Curve    elliptic.Curve
	MsgBound int
}

type SecretKey struct {
	Pk *PublicKey
	Sk *big.Int
}

func KeyGen(curve elliptic.Curve, msgBound int) (*PublicKey, *SecretKey) {
	k, x, y, _ := elliptic.GenerateKey(curve, crand.Reader)
	p, _ := ec.NewPoint(curve, x, y)
	sk := new(big.Int).SetBytes(k)
	pk := &PublicKey{Pk: p, Curve: curve, MsgBound: msgBound}
	return pk, &SecretKey{Pk: pk, Sk: sk}
}
