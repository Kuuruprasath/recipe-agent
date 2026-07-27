'use client'; // Required for using form state and file selection
import { useState, ChangeEvent, FormEvent, useRef} from 'react';


export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [statusMessage, setStatusMessage] = useState<string>('');
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle file selection from the input field
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }

  };

  // Handle form submission to FastAPI backend
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!file) {
      setStatusMessage('Please select a file first.');
      return;
    }

    setIsUploading(true);
    setStatusMessage('Uploading to your Kitchen Agent...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setStatusMessage(`Success! File saved as: ${data.filename}`);
        await new Promise((resolve) => setTimeout(resolve, 3000));
        setStatusMessage('');
        setFile(null); 
        if (fileInputRef.current) {
          fileInputRef.current.value = ""; 
        }
        
      } else {
        setStatusMessage(`Upload failed: ${data.detail || 'Unknown error'}`);
      }
    } catch (error) {
      setStatusMessage('Network error. Check if your FastAPI server is running.');
    } finally {
      setIsUploading(false);
    } 
  };

  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-zinc-50 font-sans dark:bg-black min-h-screen">
      <main className="flex flex-1 w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start gap-12">
        
        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
            Smart Kitchen Agent
          </h1>
          <p className="max-w-md text-lg leading-8 text-zinc-600 dark:text-zinc-400">
            The only assistant you need in the kitchen
          </p>
        </div>

        <div className="w-full max-w-md bg-zinc-50 dark:bg-zinc-900/50 p-6 rounded-2xl border border-zinc-200 dark:border-zinc-800">
          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <div className="flex flex-col gap-2">
              <label htmlFor="file-input" className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                Upload a recipe photo or document:
              </label>
              <input 
                ref={fileInputRef}
                id="file-input" 
                type="file" 
                onChange={handleFileChange}
                className="w-full text-sm text-zinc-500 dark:text-zinc-400
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-full file:border-0
                  file:text-sm file:font-semibold
                  file:bg-zinc-900 file:text-white 
                  dark:file:bg-zinc-100 dark:file:text-zinc-900
                  hover:file:opacity-90 file:cursor-pointer"
              />
            </div>

            <button 
              type="submit" 
              disabled={isUploading || !file}
              className={`w-full py-2.5 px-4 rounded-xl text-sm font-medium transition-all
                ${file && !isUploading 
                  ? 'bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900 hover:opacity-90 shadow-sm' 
                  : 'bg-zinc-200 text-zinc-400 dark:bg-zinc-800 dark:text-zinc-600 cursor-not-allowed'
                }`}
            >
              {isUploading ? 'Saving locally...' : 'Submit File'}
            </button>
          </form>

          {statusMessage && (
            <p className={`mt-4 text-sm font-medium ${statusMessage.startsWith('Success') ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
              {statusMessage}
            </p>
          )}
        </div>
        
        
      </main>
    </div>
  );
}
