const socket = io();

socket.on('connect', function() {
    console.log('Connected to server');
});

socket.on('download_progress', function(data) {
    console.log('Download progress event received', data);
    const percent = cleanProgressString(data.percent.trim());
    const progress = parseFloat(percent.replace('%', ''));
    $('#progress-bar').css('width', progress + '%').attr('aria-valuenow', progress);
    $('#progress-bar').text(percent);
    $('#progress-percent').text(percent);
});

socket.on('download_finished', function(data) {
    console.log('Download finished event received', data);
    showDownloadFinishedPopup(data.message);
});

function showDownloadFinishedPopup(message) {
    console.log('Showing SweetAlert2 popup');
    Swal.fire({
        title: "Download Concluído!",
        text: "Seu download foi feito e seu arquivo foi salvo na pasta de Download do seu computador. Deseja baixar outro arquivo?",
        icon: "success",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        cancelButtonText: "Não",
        confirmButtonText: "Sim"
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/'; // Volta para a página inicial
        } else {
            Swal.fire({
                title: "Obrigada!",
                text: "",
                icon: "success"
            });
        }
    });
}

function cleanProgressString(progressString) {
    // Remove ANSI escape codes and other unwanted characters
    return progressString.replace(/\x1b\[[0-9;]*m/g, '');
}
