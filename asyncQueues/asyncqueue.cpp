#include <iostream>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>

template <typename T>
class AsyncQueue {
public:
    void Enqueue(const T& item) {
        std::unique_lock<std::mutex> lock(mutex_);
        queue_.push(item);
        lock.unlock();
        condition_.notify_one(); // signal waiting threads
    }

    T Dequeue() {
        std::unique_lock<std::mutex> lock(mutex_);
        condition_.wait(lock, [this] { return !queue_.empty(); }); // wait for a non-empty queue

        T item = queue_.front();
        queue_.pop();
        return item;
    }

private:
    std::queue<T> queue_;
    std::mutex mutex_;
    std::condition_variable condition_;
};

int main() {
    AsyncQueue<int> asyncQueue;

    std::thread producer([&]() {
        for (int i = 0; i < 10; ++i) {
            asyncQueue.Enqueue(i);
            std::cout<<"Enque"<<std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    });

    std::thread consumer([&]() {
        for (int i = 0; i < 10; ++i) {
            int item = asyncQueue.Dequeue();
            std::cout << "Dequeued: " << item << std::endl;
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    });

    producer.join();
    consumer.join();

    return 0;
}
