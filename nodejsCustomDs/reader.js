const url = "https://example.com/some/streaming/endpoint";

fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error(`Request failed with status: ${response.status}`);
    }

    const reader = response.body.getReader();

    //recursive  function to read and process a single chunk
    function readChunk() {
      return reader.read().then(({ done, value }) => {
        if (done) {
          console.log("Stream processing complete.");
          return;
        }

        reader.pause(); //

        console.log(`Received a chunk of ${value.length} bytes.`);

        setTimeout(() => {
          reader.resume();
          readChunk();
        }, 1000);
      });
    }

    return readChunk();
  })
  .catch(error => {
    console.error("Error:", error);
  });
