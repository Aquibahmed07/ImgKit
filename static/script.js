async function handleForm(formId, endpoint, downloadId) {
  document.getElementById(formId).addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const response = await fetch(endpoint, {
      method: 'POST',
      body: formData
    });
    const blob = await response.blob();
    const contentDisposition = response.headers.get('Content-Disposition');
    let filename = 'download';
    if (contentDisposition && contentDisposition.indexOf('filename=') !== -1) {
      filename = contentDisposition.split('filename=')[1].replace(/"/g, '');
    }
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.textContent = 'Download';
    document.getElementById(downloadId).innerHTML = '';
    document.getElementById(downloadId).appendChild(link);
  });
}

handleForm('jpg2pdfForm', '/convert/jpg2pdf', 'jpg2pdfDownload');
handleForm('png2jpgForm', '/convert/png2jpg', 'png2jpgDownload');
handleForm('compressForm', '/convert/compress', 'compressDownload');
handleForm('rotateForm', '/convert/rotate', 'rotateDownload');
handleForm('cropForm', '/convert/crop', 'cropDownload');
handleForm('jpg2pnggifForm', '/convert/jpg2pnggif', 'jpg2pnggifDownload');
handleForm('watermarkForm', '/convert/watermark', 'watermarkDownload');
handleForm('removebgForm', '/convert/removebg', 'removebgDownload');

document.getElementById('resizeForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const formData = new FormData(this);
  const response = await fetch('/convert/resize', {
    method: 'POST',
    body: formData
  });
  const blob = await response.blob();
  const contentDisposition = response.headers.get('Content-Disposition');
  let filename = 'resized.zip';
  if (contentDisposition && contentDisposition.indexOf('filename=') !== -1) {
    filename = contentDisposition.split('filename=')[1].replace(/"/g, '');
  }
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.textContent = 'Download';
  document.getElementById('resizeDownload').innerHTML = '';
  document.getElementById('resizeDownload').appendChild(link);
});
