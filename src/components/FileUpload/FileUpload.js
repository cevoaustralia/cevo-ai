import React, { useState, useEffect } from 'react';

function FileUpload({ domain = 'default' }) {
  const [file, setFile] = useState(null);
  const [files, setFiles] = useState([]);

  const fetchFiles = async () => {
    try {
      const response = await fetch(`http://localhost:5000/files/${domain}`);
      const data = await response.json();
      setFiles(data.files);
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, [domain]);

  const handleUpload = async () => {
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('domain', domain);
    
    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        alert('File uploaded successfully!');
        setFile(null);
        fetchFiles();
      } else {
        alert('Upload failed');
      }
    } catch (error) {
      alert('Upload error');
    }
  };

  const handleDelete = async (filename) => {
    try {
      const response = await fetch(`http://localhost:5000/files/${domain}/${filename}`, {
        method: 'DELETE',
      });
      
      if (response.ok) {
        fetchFiles();
      } else {
        alert('Delete failed');
      }
    } catch (error) {
      alert('Delete error');
    }
  };

  return (
    <div className="file-upload">
      <h3>Upload Files</h3>
      <input 
        type="file" 
        onChange={(e) => setFile(e.target.files[0])}
        accept=".pdf,.jpg,.jpeg,.png"
      />
      <button onClick={handleUpload} disabled={!file}>Upload</button>
      
      <table style={{marginTop: '20px', width: '100%', borderCollapse: 'collapse'}}>
        <thead>
          <tr>
            <th style={{border: '1px solid #ccc', padding: '8px'}}>Files in {domain}</th>
            <th style={{border: '1px solid #ccc', padding: '8px', width: '60px'}}>Delete</th>
          </tr>
        </thead>
        <tbody>
          {files.map((fileName, index) => (
            <tr key={index}>
              <td style={{border: '1px solid #ccc', padding: '8px'}}>{fileName}</td>
              <td style={{border: '1px solid #ccc', padding: '8px', textAlign: 'center'}}>
                <button 
                  onClick={() => handleDelete(fileName)}
                  style={{background: 'none', border: 'none', cursor: 'pointer', fontSize: '16px'}}
                >
                  🗑️
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FileUpload;