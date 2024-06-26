package rpcBench

import (
	"context"
	"runtime/trace"
	"testing"
)

type Server any

const NUM_TESTS = 5

type Request interface {
	Make()
	Get() string
}

type Result interface {
	Get() string
}

type Ptr[T any] interface {
	*T
	Request
}

func NewRequest[T Ptr[R], R any]() T {
	var r R
	t := T(&r)
	t.Make()
	return t
}

type RPCFunc func(context.Context, Server) (Request, Result, error)

func (rpc RPCFunc) Test(ctx context.Context, s Server, t *testing.T, testName string) {
	for i := 0; i < NUM_TESTS; i++ {
		req, res, err := rpc(ctx, s)
		if err != nil {
			t.Error(err.Error())
		}
		WriteTestResults(testName, req.Get(), res.Get())
	}
}

func (rpc RPCFunc) Bench(ctx context.Context, s Server, b *testing.B, benchName string) {
	if trace.IsEnabled() {
		name := benchName + " Concurrent"
		b.Run(name, func(b *testing.B) {
			for i := 0; i < b.N; i++ {
				ctx, task := trace.NewTask(ctx, name)
				trace.Log(ctx, name, name+" Begin")
				_, _, err := rpc(ctx, s)
				trace.Log(ctx, name, name+" End")
				task.End()

				if err != nil {
					b.Error(err.Error())
				}
			}
		})
		name = benchName + " Parallel"
		b.Run(name, func(b *testing.B) {
			b.RunParallel(func(pb *testing.PB) {
				for pb.Next() {

					ctx, task := trace.NewTask(ctx, name)
					trace.Log(ctx, name, name+" Begin")
					_, _, err := rpc(ctx, s)
					trace.Log(ctx, name, name+" End")
					task.End()

					if err != nil {
						b.Error(err.Error())
					}
				}
			})
		})
	} else {
		b.Run(benchName+" Concurrent", func(b *testing.B) {
			for i := 0; i < b.N; i++ {

				_, _, err := rpc(ctx, s)
				if err != nil {
					b.Error(err.Error())
				}
			}
		})
		b.Run(benchName+" Parallel", func(b *testing.B) {
			b.RunParallel(func(pb *testing.PB) {
				for pb.Next() {
					_, _, err := rpc(ctx, s)
					if err != nil {
						b.Error(err.Error())
					}
				}
			})
		})
	}

}
