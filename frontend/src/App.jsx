import { useState } from 'react';
import './App.css';

function App() {
  const [inputCode, setInputCode] = useState('');
  const [refactoredCode, setRefactoredCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copyButtonText, setCopyButtonText] = useState('Copy');

  const handleRefactor = async () => {
    setIsLoading(true);
    setRefactoredCode('');
    setCopyButtonText('Copy');
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: inputCode }),
      });
      const data = await response.json();
      setRefactoredCode(data.error || data.refactored_code);
    } catch (error) {
      console.error("Failed to fetch:", error);
      setRefactoredCode("Failed to connect to the backend. Is the Python server running?");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(refactoredCode);
    setCopyButtonText('Copied!');
    setTimeout(() => setCopyButtonText('Copy'), 2000);
  };

  return (
    <div className="App">
      <h1>AI Code Assistant</h1>
      <p>Paste your code below to get a refactored version.</p>
      
      {/* This container will handle our centering and layout logic */}
      <div className="contentContainer">
        <div className="column">
          <h2>Your Code:</h2>
          <textarea
            className="codeInput"
            value={inputCode}
            onChange={(e) => setInputCode(e.target.value)}
            placeholder="Your code here..."
          />
        </div>

        {refactoredCode && (
          <div className="column">
            <div className="resultHeader">
              <h2>Result:</h2>
              <button onClick={handleCopy} className="copyButton">{copyButtonText}</button>
            </div>
            <pre className="codeOutput">
              <code>{refactoredCode}</code>
            </pre>
          </div>
        )}
      </div>
      
      <button className="refactorButton" onClick={handleRefactor} disabled={isLoading || !inputCode}>
        {isLoading ? 'Analyzing...' : 'Refactor Code'}
      </button>
    </div>
  )
}

export default App;