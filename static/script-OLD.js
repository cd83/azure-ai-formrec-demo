function uploadFile() {
    let fileInput = document.getElementById('fileInput');
    let file = fileInput.files[0];
    
    let formData = new FormData();
    formData.append('file', file);

    fetch('/classify', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('results').innerText = JSON.stringify(data);
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById('dropArea').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function() {
    document.getElementById('dropArea').innerText = this.files[0].name;
});

// Add drag and drop functionality as needed
