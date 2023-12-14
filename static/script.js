function uploadFile() {
    let fileInput = document.getElementById('fileInput');
    let file = fileInput.files[0];
    
    let formData = new FormData();
    formData.append('file', file);

    // Show loading indicator
    document.getElementById('loading').style.display = 'block';

    fetch('/classify', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading indicator
        document.getElementById('loading').style.display = 'none';

        let resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = ''; // Clear previous results

        data.forEach(doc => {
            let resultDiv = document.createElement('div');
            resultDiv.classList.add('doc-result');

            let type = document.createElement('p');
            type.textContent = `Type: ${doc.type}`;

            let confidence = document.createElement('p');
            confidence.textContent = `Confidence: ${doc.confidence.toFixed(2)}`;

            let pages = document.createElement('p');
            pages.textContent = `Pages: ${doc.pages.join(', ')}`;

            resultDiv.appendChild(type);
            resultDiv.appendChild(confidence);
            resultDiv.appendChild(pages);

            resultsContainer.appendChild(resultDiv);
        });
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('results').innerText = 'Error processing the file.';
        // Hide loading indicator
        document.getElementById('loading').style.display = 'none';
    });
}



document.getElementById('dropArea').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function() {
    document.getElementById('dropArea').innerText = this.files[0].name;
});

// Add drag and drop functionality as needed
