import React, { useState } from 'react';

function FileUpload() {
  const [file, setFile] = useState(null);

  return (
    <div className="file-upload">
      <h3>Upload Files</h3>
      <input 
        type="file" 
        onChange={(e) => setFile(e.target.files[0])}
        accept=".pdf,.jpg,.jpeg,.png"
      />
      <button>Upload</button>
    </div>
  );
}

export default FileUpload;