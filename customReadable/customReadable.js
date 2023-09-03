const { Readable } = require("stream");
//Readables are great
class CustomReadable extends Readable {
  constructor(array) {
    super({ objectMode: true });
    this.array = array;
    this.index = 0;
  }
// this would be called by iterator or when the stream processor is ready to process next chunk
// so basically in the beggining of each iteration this would be called.
  _read() {
    if (this.index < this.array.length) {
      const data = this.array[this.index];
      this.push(data);
      this.index++;
    } else {
      this.push(null);
    }
  }
}

const dataArray = [
  { choices: [{ delta: { content: "Chunk 1" } }] },
  { choices: [{ delta: { content: "Chunk 2" } }] },
  { choices: [{ delta: { content: "Chunk 3" } }] },
];

const customStream = new CustomReadable(dataArray);

async function processData() {
  for await (const part of customStream) {
    process.stdout.write(part.choices[0]?.delta?.content || "");
  }
}

processData().catch((error) => console.error(error));
