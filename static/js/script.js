document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const resultImage = document.getElementById('resultImage');
    const detectionText = document.getElementById('detectionText');
    const placeholder = document.querySelector('.placeholder');
    const fileInput = document.getElementById('fileInput');
    const fileName = document.getElementById('fileName');
    const uploadBtn = document.getElementById('uploadBtn');
    const startCamera = document.getElementById('startCamera');
    const takeSnapshot = document.getElementById('takeSnapshot');
    const toggleLive = document.getElementById('toggleLive');
    const liveStatus = document.getElementById('liveStatus');

    let stream = null;
    let liveInterval = null;
    let isLive = false;
    let hasCamera = false;

    // File selection & upload
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileName.textContent = 'File selected';
            uploadBtn.disabled = false;
        }
    });

    uploadBtn.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        sendToServer(formData, true);  // true = from upload
        fileInput.value = '';
        fileName.textContent = '';
        uploadBtn.disabled = true;
    });

    // Start camera
    startCamera.addEventListener('click', async () => {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            hasCamera = true;
            takeSnapshot.disabled = false;
            toggleLive.disabled = false;
            startCamera.disabled = true;
            detectionText.textContent = 'Camera ready. Try snapshot or live.';
        } catch (err) {
            hasCamera = false;
            detectionText.textContent = 'No camera found or access denied. Use image upload only.';
            takeSnapshot.disabled = true;
            toggleLive.disabled = true;
            toggleLive.textContent = 'Start Live Detection';
            liveStatus.textContent = '';
        }
    });

    // Snapshot
    takeSnapshot.addEventListener('click', () => captureAndSend());

    // Live toggle
    toggleLive.addEventListener('click', () => {
        if (!hasCamera) return;

        if (isLive) {
            stopLive();
        } else {
            isLive = true;
            toggleLive.textContent = 'Stop Live Detection';
            liveStatus.textContent = 'LIVE';
            captureAndSend();
            liveInterval = setInterval(captureAndSend, 1000);
        }
    });

    function stopLive() {
        clearInterval(liveInterval);
        isLive = false;
        toggleLive.textContent = 'Start Live Detection';
        liveStatus.textContent = '';
    }

    function captureAndSend() {
        if (!hasCamera || video.videoWidth === 0) {
            stopLive();
            detectionText.textContent = 'Camera not ready.';
            return;
        }
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        const dataURL = canvas.toDataURL('image/jpeg', 0.9);

        const formData = new FormData();
        formData.append('image', dataURL);
        sendToServer(formData);
    }

    function sendToServer(formData, isUpload = false) {
        placeholder.style.display = 'none';
        detectionText.textContent = 'Processing...';
        resultImage.style.display = 'none';

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                detectionText.textContent = data.error;
                if (isLive) stopLive();  // Auto-stop live on error
            } else {
                resultImage.src = data.image_url + '?' + new Date().getTime();
                resultImage.style.display = 'block';
                detectionText.textContent = data.detections;
                if (isLive && data.success) {
                    // Optional: keep live running, or stop on first success
                    // Currently keeps running for continuous detection
                }
                if (isUpload && isLive) stopLive();  // Stop live if upload used
            }
        })
        .catch(err => {
            detectionText.textContent = 'Connection error. Try again.';
            if (isLive) stopLive();
        });
    }
});
