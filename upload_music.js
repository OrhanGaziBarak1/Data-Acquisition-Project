const url = 'process.php';
const form = document.querySelector('form');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const files = document.querySelector('[type=file]').files;
  const formData = new FormData();

  for (let i = 0; i < files.length; i++) {
    let file = files[i];
    formData.append('files[]', file);
  }

  fetch(url, {
    method: 'POST',
    body: formData,
  })
    .then((response) => {
      // Check if the response status is in the range 200-299 (success)
      if (response.ok) {
        return response.json(); // Parse the JSON data from the response
      } else {
        throw new Error(`Error: ${response.statusText}`);
      }
    })
    .then((data) => {
      // Data will contain the response from the server
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
});
