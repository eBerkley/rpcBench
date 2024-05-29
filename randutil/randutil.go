package randutil

import (
	"context"
	"flag"
	"math/rand"
)

var rand_seed = flag.Int64("seed", 55, "Seed used for rng")

const BUF_SIZE = 99999

type RandSeed struct {
	seed *rand.Rand
	next chan float32
	ctx  context.Context
}

func (rs *RandSeed) randWorker() {
	for {
		nextRand := rs.seed.Float32()

		select {
		case <-rs.ctx.Done():
			return
		case rs.next <- nextRand:
			// continue
		}
	}
}

func NewRandSeed(bufSize int) *RandSeed {
	rs := new(RandSeed)
	rs.seed = rand.New(rand.NewSource(*rand_seed))
	rs.next = make(chan float32, bufSize)
	rs.ctx = context.Background()

	go rs.randWorker()
	return rs
}

func (rs *RandSeed) GetNext() (float32, bool) {
	c, ok := <-rs.next
	return c, ok

	// return rs.seed.Float32(), true
}

var r *RandSeed

func SetR() {
	r = NewRandSeed(BUF_SIZE)
}

func Random(f float32) float32 {
	c, _ := r.GetNext()
	return c * f
	// return rand.Float32() * f
}
