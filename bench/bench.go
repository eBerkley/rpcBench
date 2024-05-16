package bench

import (
	"context"
	"testing"
)

type Server any

type Benchable func(context.Context, Server) error

func (b Benchable) call(ctx context.Context, s Server) error {
	return b(ctx, s)
}

func RunSubBenchmarks(name string, b *testing.B, bnch Benchable, ctx context.Context, s Server) {
	b.Run(name+" Concurrent", func(b *testing.B) {
		for i := 0; i < b.N; i++ {
			err := bnch(ctx, s)
			if err != nil {
				b.Error(err.Error())
			}
		}
	})
	b.Run(name+" Parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				err := bnch(ctx, s)
				if err != nil {
					b.Error(err.Error())
				}
			}
		})
	})
}
