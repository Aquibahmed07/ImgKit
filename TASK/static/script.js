async function handleFormSubmit(formId, endpoint, defaultFilename) {
    const form = document.getElementById(formId);
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          body: formData
        });
        if (!response.ok) {
          alert('Failed to process images.');
          return;
        }
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = defaultFilename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } catch (err) {
        alert('Error: ' + err.message);
      }
    });
  }

  handleFormSubmit('compressForm', '/convert/compress', 'compressed.zip');
  handleFormSubmit('resizeForm', '/convert/resize', 'resized.zip');
  handleFormSubmit('cropForm', '/convert/crop', 'cropped.zip');
  handleFormSubmit('png2jpgForm', '/convert/jpg', 'converted_jpg.zip');
  handleFormSubmit('jpg2pnggifForm', '/convert/jpg2pnggif', 'converted.zip');
  handleFormSubmit('removebgForm', '/convert/removebg', 'nobg.zip');
  handleFormSubmit('watermarkForm', '/convert/watermark', 'watermarked.zip');
  handleFormSubmit('rotateForm', '/convert/rotate', 'rotated.zip');

  handleFormSubmit('upscaleForm', '/convert/upscale', 'upscaled.zip');
  handleFormSubmit('bmpForm', '/convert/bmp', 'converted_bmp.zip');
  handleFormSubmit('pagForm', '/convert/pag', 'converted_pag.zip');
  handleFormSubmit('pdfForm', '/convert/pdf', 'converted.pdf');

