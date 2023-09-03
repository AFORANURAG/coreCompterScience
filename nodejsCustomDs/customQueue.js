// implement a custom queue which would poll, publish and consume message in poll time and also sends message whenever an element is added to it
const crypto = require("crypto");
const { EventEmitter} = require("events")
const eventListener = new EventEmitter()
class CustomQueue extends EventEmitter {
  constructor() {
    super()
    this.queue = []
    this.timerIds = [];
    this.dequeueIndex = 0
  }
  // listener
  // how multiple listener
  async consume(processor,pollTime) {
    // either pass it as a callback or pass it during instantiation.
  if(!this.queue.length){
  let id = setInterval(()=>{
    const dataToProcess = this.queue[this.dequeueIndex];
     processor(dataToProcess).then((response)=>{
       if(!response.success){
         this.emit(`dataProccessingFailed`,dataToProcess)
         // when you are adding data to it , try to to add a unique hash also with
         return
       }
   this.timerIds.push(id)
      this.dequeueIndex++
     });

  },pollTime)
    // rather than dequequing, try to maintain a dequeue pointer
  }
    return 0
  }

  publish(element) {
    this.queue.push({element,id:this.hashGenerator()})
    this.emit("elementAdded", element)
  }

  hashGenerator(){
    // create a random number and then convert it to a base 36 string
    let randomString  = Math.random().toString(36)
    let hash = crypto.createHash('sha256')

    hash.update(randomString)
    let hashedString = hash.digest('hex');
    return hashedString
  }

  close(){
    this.timerIds.forEach((el)=>{
      clearIntervalId(el)
    })
  }
  printAll(){
    this.queue.forEach((el)=>{
      console.log(el)
    })
  }
}
let customQueue = new CustomQueue();
customQueue.on('elementAdded',(data)=>{
  console.log('element added',data)
})
customQueue.publish(10)
customQueue.publish(10)
customQueue.printAll()

const stringToSend = "Hello from the main thread!";
const encodedData = Buffer.from(stringToSend, 'utf-8');
console.log(encodedData)
