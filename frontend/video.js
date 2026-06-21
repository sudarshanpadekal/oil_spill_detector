document.addEventListener('DOMContentLoaded', () => {
  const videoInput = document.getElementById('video-input');
  const processBtn = document.getElementById('process-video-btn');
  const videoResultPanel = document.getElementById('video-result-panel');
  const videoLoader = document.getElementById('video-loader');
  const videoStatus = document.getElementById('video-status');
  const videoOutput = document.getElementById('video-output');

  processBtn.addEventListener('click', async () => {
    const file = videoInput.files[0];
    if (!file) {
      videoStatus.textContent = 'Please choose a video file first.';
      videoStatus.className = 'result-text warning';
      videoResultPanel.classList.remove('hidden');
      return;
    }

    videoResultPanel.classList.remove('hidden');
    videoLoader.classList.remove('hidden');
    videoStatus.textContent = 'Processing video...';
    videoStatus.className = 'result-text';
    videoOutput.classList.add('hidden');
    processBtn.disabled = true;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/video-detect', { method: 'POST', body: formData });
      if (!response.ok) throw new Error('Unable to process video');

      const data = await response.json();
      if (data.status === 'success') {
        videoStatus.textContent = data.message;
        videoStatus.className = 'result-text success';
      } else {
        throw new Error('Processing failed');
      }
    } catch (error) {
      videoStatus.textContent = 'Video processing failed.';
      videoStatus.className = 'result-text warning';
      console.error(error);
    } finally {
      videoLoader.classList.add('hidden');
      processBtn.disabled = false;
    }
  });
});
