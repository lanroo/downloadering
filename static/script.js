const socket = io();

socket.on('connect', function() {
    console.log('Conectado ao servidor');
});

socket.on('download_progress', function(data) {
    const progressBar = document.getElementById('progress-bar');
    const cleanedPercent = cleanProgressString(data.percent.trim());
    const progress = parseFloat(cleanedPercent.replace('%', ''));
    progressBar.style.width = progress + '%';
    progressBar.setAttribute('aria-valuenow', progress);
    progressBar.textContent = progress + '%';
    document.getElementById('progress-percent').textContent = cleanedPercent;
});

socket.on('download_finished', function(data) {
    const filePath = encodeURIComponent(data.file_path);
    window.location.href = `/download/${filePath}`;
    setTimeout(() => {
        Swal.fire({
            title: 'Obrigado!',
            text: 'Deseja baixar mais algum arquivo?',
            icon: 'success',
            showCancelButton: true,
            confirmButtonText: 'Sim',
            cancelButtonText: 'Não'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '/';
            }
        });
    }, 3000);
});

function cleanProgressString(progressString) {
    return progressString.replace(/\x1b\[([0-9;]*)m/g, '').replace(/[^\x20-\x7E]/g, '');
}
