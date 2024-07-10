const socket = io();

socket.on('connect', function() {
    console.log('Connected to server');
});

socket.on('download_progress', function(data) {
    console.log('Download progress event received', data);
    const cleanedPercent = cleanProgressString(data.percent.trim());
    const progress = parseFloat(cleanedPercent.replace('%', ''));
    $('#progress-bar').css('width', progress + '%').attr('aria-valuenow', progress);
    $('#progress-bar').text(progress + '%'); // Exibir apenas a porcentagem limpa na barra
    $('#progress-percent').text(cleanedPercent);
});

socket.on('download_finished', function(data) {
    console.log('Download finished event received', data);
    const filePath = encodeURIComponent(data.file_path);
    window.location.href = `/download/${filePath}`;
    // Mostrar popup de agradecimento após um breve atraso para garantir que o download seja iniciado
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
                window.location.href = '/'; // Volta para a página inicial
            }
        });
    }, 3000); // 3 segundos de atraso
});

function cleanProgressString(progressString) {
    // Remove ANSI escape codes and other unwanted characters
    return progressString.replace(/\x1b\[([0-9;]*)m/g, '').replace(/[^\x20-\x7E]/g, '');
}

document.addEventListener('DOMContentLoaded', function () {
    const socket = io();

    socket.on('download_progress', function (data) {
        const progressBar = document.getElementById('progress-bar');
        const cleanedPercent = cleanProgressString(data.percent.trim());
        const progress = parseFloat(cleanedPercent.replace('%', ''));
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('aria-valuenow', progress);
        progressBar.textContent = progress + '%';
        document.getElementById('progress-percent').textContent = cleanedPercent;
    });

    socket.on('download_finished', function (data) {
        const filePath = encodeURIComponent(data.file_path);
        window.location.href = `/download/${filePath}`;
        // Mostrar popup de agradecimento após um breve atraso para garantir que o download seja iniciado
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
                    window.location.href = '/'; // Volta para a página inicial
                }
            });
        }, 3000); // 3 segundos de atraso
    });
});
