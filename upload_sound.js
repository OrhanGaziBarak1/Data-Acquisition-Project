function handleSubmit(event) {
    event.preventDefault();
  
    showPendingState();
  
    try {
      // Dosya türlerini kontrol etmek için asenkron bir işleme ihtiyaç yok
      assertFilesValid(fileInput.files);
      // Dosyaları yüklemek için asenkron işlem başlat
      uploadFiles();
    } catch (err) {
      updateStatusMessage(err.message);
    }
  }
  
  // ...
  
  function assertFilesValid(fileList) {
    const sizeLimit = 50 * 1024 * 1024; // 50 megabytes
    let valid = true;
  
    for (const file of fileList) {
      const { name: fileName, size: fileSize } = file;
  
      // Dosya türünü kontrol etmek için callback kullanma
      const realType = getRealFileTypeSync(file);
  
      if (realType !== 'audio/mp3') {
        valid = false;
        throw new Error(
          `❌ File "${fileName}" could not be uploaded. Only files with the following types are allowed: MP3.`,
        );
      }
  
      if (fileSize > sizeLimit) {
        valid = false;
        throw new Error(
          `❌ File "${fileName}" could not be uploaded. Only files up to 50 MB are allowed.`,
        );
      }
    }
  
    return valid;
  }
  
  function getRealFileTypeSync(file) {
    const reader = new FileReaderSync();
    const arr = (new Uint8Array(reader.readAsArrayBuffer(file))).subarray(0, 4);
    let header = '';
    for (let i = 0; i < arr.length; i++) {
      header += arr[i].toString(16);
    }
  
    // Bu örnekte sadece MP3 dosyalarını kontrol ediyoruz
    if (header === '49443304') {
      return 'audio/mp3';
    } else {
      return null;
    }
  }
  function handleSubmit(event) {
    event.preventDefault();
  
    showPendingState();
  
    try {
      // Dosya türlerini kontrol etmek için asenkron bir işleme ihtiyaç yok
      assertFilesValid(fileInput.files);
      // Dosyaları yüklemek için asenkron işlem başlat
      uploadFiles();
    } catch (err) {
      updateStatusMessage(err.message);
    }
  }
  
  // ...
  
  function assertFilesValid(fileList) {
    const sizeLimit = 50 * 1024 * 1024; // 50 megabytes
    let valid = true;
  
    for (const file of fileList) {
      const { name: fileName, size: fileSize } = file;
  
      // Dosya türünü kontrol etmek için callback kullanma
      const realType = getRealFileTypeSync(file);
  
      if (realType !== 'audio/mp3') {
        valid = false;
        throw new Error(
          `❌ File "${fileName}" could not be uploaded. Only files with the following types are allowed: MP3.`,
        );
      }
  
      if (fileSize > sizeLimit) {
        valid = false;
        throw new Error(
          `❌ File "${fileName}" could not be uploaded. Only files up to 50 MB are allowed.`,
        );
      }
    }
  
    return valid;
  }
  
  function getRealFileTypeSync(file) {
    const reader = new FileReaderSync();
    const arr = (new Uint8Array(reader.readAsArrayBuffer(file))).subarray(0, 4);
    let header = '';
    for (let i = 0; i < arr.length; i++) {
      header += arr[i].toString(16);
    }
  
    // Bu örnekte sadece MP3 dosyalarını kontrol ediyoruz
    if (header === '49443304') {
      return 'audio/mp3';
    } else {
      return null;
    }
  }
    