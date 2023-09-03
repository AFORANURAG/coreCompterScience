const { Worker } = require("worker_threads");
const buffer = Buffer.alloc(5);
const array = new Uint8Array(buffer);
array.fill(5);
const worker = new Worker("./.js", { workerData: buffer });
worker.on("message", () => {
  console.log("done");
});
console.log("hello world");
// if you are experienced enough you would know what is going to run in a seperate thread or not.
// (async ()=>{
// await new Promise((resolve, reject) => {
//   setTimeout(resolve, 100, 'foo');
//   console.log("sahi hai")
// }).then((val)=>console.log(val));
// })()
// console.log("hello")
