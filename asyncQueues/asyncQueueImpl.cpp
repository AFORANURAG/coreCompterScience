// #include <iostream>
// #include <queue>
// #include <thread>
// #include <mutex>
// #include <condition_variable>

// template <typename T>
// class AsyncQueue {
//     public:
//       void Enqueue(const T& item){
//         std::unique_lock<std::mutex>lock(mutex);
//         queue_.push(item);
//         lock.unlock();
//         condition_.notify_one();
//       }

//       T Dequeue(){
//         std::unique_lock<std::mutex> lock(mutex);
//         condition_.wait(lock,[this]{return !queue_.empty();});
//         T item = queue_.front();
//         queue_.pop();
//         return item;
//       }

// private:
//   std::queue<T> queue_;
//   std::mutex mutex;
//   std::condition_variable condition_;
// };

// int main(){
// AsyncQueue<int> asyncQueue;

// std::thread producer ([&](){
//     for(int i=0;i<10;i++){
//     asyncQueue.Enqueue(i);
//     std::cout<<"Enque"<<std::endl;
//     std::this_thread::sleep_for(std::chrono::milliseconds(500));
//     }

// });
// // std::thread producer1 ([&](){
// //     for(int i=10;i<20;i++){
// //     asyncQueue.Enqueue(i);
// //     std::cout<<"Enque"<<std::endl;
// //     std::this_thread::sleep_for(std::chrono::milliseconds(500));
// //     }

// // });




//  std::thread consumer([&]() {
//         for (int i = 0; i < 10; ++i) {
//             int item = asyncQueue.Dequeue();
//             std::cout << "Dequeued: " << item << std::endl;
//             std::this_thread::sleep_for(std::chrono::milliseconds(500));
//         }
// });
//  std::thread consumer1([&]() {
//         for (int i = 0; i < 10; ++i) {
//             int item = asyncQueue.Dequeue();
//             std::cout << "Dequeued: " << item << std::endl;
//             std::this_thread::sleep_for(std::chrono::milliseconds(500));
//         }
// });
// // producer1.join();
// producer.join();
// consumer.join();
// consumer1.join();
   
// };



#include <iostream>
#include <vector>
#include <thread>
#include <mutex>
#include <condition_variable>

template <typename T>
class AsyncQueue {
public:
    AsyncQueue(size_t capacity) : capacity_(capacity), queue_(capacity), front_(0), rear_(0), size_(0) {}

    bool Enqueue(const T& item) {
        std::unique_lock<std::mutex> lock(mutex_);
        
        if (size_ >= capacity_) {
            // Queue is full, cannot enqueue.
            return false;
        }

        queue_[rear_] = item;
        rear_ = (rear_ + 1) % capacity_;
        size_++;

        condition_.notify_one();
        return true;
    }

    bool Dequeue(T& item) {
        std::unique_lock<std::mutex> lock(mutex_);

        if (size_ == 0) {
            // Queue is empty, cannot dequeue.
            return false;
        }

        item = queue_[front_];
        front_ = (front_ + 1) % capacity_;
        size_--;

        condition_.notify_one();
        return true;
    }

private:
    size_t capacity_;
    std::vector<T> queue_;
    size_t front_;
    size_t rear_;
    size_t size_;
    std::mutex mutex_;
    std::condition_variable condition_;
};

int main() {
    AsyncQueue<int> asyncQueue(10);

    std::thread producer([&]() {
        for (int i = 0; i < 15; i++) {
            if (asyncQueue.Enqueue(i)) {
                std::cout << "Enqueued: " << i << std::endl;
            } else {
                std::cout << "Queue is full, unable to enqueue: " << i << std::endl;
            }
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    });

    std::thread consumer([&]() {
        int item;
        for (int i = 0; i < 15; i++) {
            if (asyncQueue.Dequeue(item)) {
                std::cout << "Dequeued: " << item << std::endl;
            } else {
                std::cout << "Queue is empty, unable to dequeue." << std::endl;
            }
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    });

    producer.join();
    consumer.join();

    return 0;
}
