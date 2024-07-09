function openFileDialog() {
    document.getElementById('fileDialog').click();
}

function setDirectoryPath() {
    const fileInput = document.getElementById('fileDialog');
    if (fileInput.files.length > 0) {
        const filePath = fileInput.files[0].webkitRelativePath;
        const directoryPath = filePath.substring(0, filePath.indexOf('/'));
        document.getElementById('download_path').value = directoryPath;
    }
}
