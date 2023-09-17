package main
import (
	"fmt"
	"sync"
	"time"
)
type AsyncQueue struct {
	queue   chan interface{}
	closeCh chan struct{}
	wg      sync.WaitGroup
}

func NewAsyncQueue(maxSize int) *AsyncQueue {
	return &AsyncQueue{
		queue:   make(chan interface{}, maxSize),
		closeCh: make(chan struct{}),
	}
}

func (aq *AsyncQueue) Enqueue(item interface{}) {
	aq.queue <- item
}

func (aq *AsyncQueue) Dequeue() interface{} {
	return <-aq.queue
}

func (aq *AsyncQueue) Close() {
	close(aq.closeCh)
	aq.wg.Wait()
	close(aq.queue)
}

func (aq *AsyncQueue) Worker() {
	defer aq.wg.Done()
	for {
		select {
		case <-aq.closeCh:
			return
		case item := <-aq.queue:
			fmt.Printf("Dequeued from %p: %v\n", aq, item)
			time.Sleep(time.Second) // Simulate processing
		}
	}
}

func main() {
	asyncQueue1 := NewAsyncQueue(5)
	asyncQueue2 := NewAsyncQueue(5)

	go asyncQueue1.Worker()
	go asyncQueue2.Worker()

	for i := 0; i < 10; i++ {
		asyncQueue1.Enqueue(i)
		asyncQueue2.Enqueue(i * 10)
		fmt.Printf("Enqueued: %v\n", i)
		time.Sleep(time.Millisecond * 500)
	}

	time.Sleep(time.Second * 3)

	asyncQueue1.Close()
	asyncQueue2.Close()
}
