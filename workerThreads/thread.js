const { parentPort, workerData } = require("worker_threads");
console.log(workerData);
for (let i = 0; i < 10000; i++) {
  // console.log("sdjklsa")
}
parentPort.postMessage("message");
