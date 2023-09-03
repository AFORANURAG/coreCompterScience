package main
// this idea and implementation has been given by robert pike, i am just explaiining and 
//reimplementing it, 
import (
	"container/heap"
	"fmt"
	"time"
)

type Worker struct {
	requests chan Request
	pending  int
	index    int
}

type Pool []*Worker

type Balancer struct {
	pool Pool
	done chan *Worker
}

type Request struct {
	fn func() int
	c  chan int
}

func (w *Worker) work(done chan *Worker) {
	for {
		req := <-w.requests
		req.c <- req.fn()
		done <- w
	}
}

func (b *Balancer) balance(work chan Request) {
	for {
		select {
		case req := <-work:
			b.dispatch(req)
		case w := <-b.done:
			b.completed(w)
		}
	}
}

func (b *Balancer) dispatch(req Request) {
	w := heap.Pop(&b.pool).(*Worker)
	w.requests <- req
	w.pending++
	heap.Push(&b.pool, w)
}

func requester(work chan<- Request) {
	c := make(chan int)
	for {
		time.Sleep(time.Millisecond * 500)
		work <- Request{workFn, c}
		result := <-c
		furtherProcess(result)
	}
}

func (b *Balancer) completed(w *Worker) {
	w.pending--
	heap.Remove(&b.pool, w.index)
	heap.Push(&b.pool, w)
}

// Placeholder functions
func workFn() int {
	return 42
}

func furtherProcess(result int) {
	fmt.Println("Processed result:", result)
}

func main() {
	poolSize := 5
	b := &Balancer{
		pool: make(Pool, poolSize),
		done: make(chan *Worker),
	}

	for i := 0; i < poolSize; i++ {
		w := &Worker{
			requests: make(chan Request),
			index:    i,
		}
		go w.work(b.done)
		b.pool[i] = w
	}

	go b.balance(make(chan Request))
	go requester(make(chan Request))

	// Run the program indefinitely
	select {}
}
