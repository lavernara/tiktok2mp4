document.getElementById('download-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const url = document.getElementById('videoUrl').value;

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.download_link) {
            document.getElementById('download-link').innerHTML = `<p>Download your video: <a href="${data.download_link}">Click here to download</a></p>`;
        } else {
            document.getElementById('download-link').innerHTML = `<p>Error: ${data.error}</p>`;
        }
    })
    .catch(error => {
        document.getElementById('download-link').innerHTML = `<p>Error: ${error.message}</p>`;
    });
});
