import { useState } from "react";
import "./App.css";


function App() {

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! Ask me about crop prices, arrivals, weather, mandi terminology, or agricultural market insights.",
      source: null,
    },
  ]);

  const [input, setInput] = useState("");

  const [isLoading, setIsLoading] = useState(false);


  const sendMessage = async (e) => {

    e.preventDefault();

    if (!input.trim() || isLoading) {
      return;
    }


    const question = input.trim();


    const userMessage = {
      role: "user",
      content: question,
      source: null,
    };


    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);


    setInput("");

    setIsLoading(true);


    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/query",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question: question,
          }),
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail || "API request failed"
        );
      }


      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            data.answer ||
            "I could not generate an answer.",

          source: data.source || null,
        },
      ]);

    } catch (error) {

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            error.message ||
            "Connection error. Ensure the FastAPI backend is running.",

          source: null,
        },
      ]);

    } finally {

      setIsLoading(false);

    }
  };


  const getSourceLabel = (source) => {

    if (source === "sql") {
      return "PostgreSQL";
    }

    if (source === "rag") {
      return "Knowledge Base";
    }

    if (source === "hybrid") {
      return "PostgreSQL + Knowledge Base";
    }

    return null;
  };


  return (

    <div className="chat-container">

      <header className="chat-header">

        <h1>
          🌾 Agri-Market Intelligence
        </h1>

        <p>
          Conversational Business Intelligence
        </p>

      </header>


      <div className="chat-box">

        {messages.map((msg, index) => (

          <div
            key={index}
            className={`message ${msg.role}`}
          >

            <div className="message-content">

              {msg.role === "assistant" &&
                msg.source && (

                  <div className="source-badge">

                    Source:{" "}
                    {getSourceLabel(
                      msg.source
                    )}

                  </div>

                )}


              <div>
                {msg.content}
              </div>

            </div>

          </div>

        ))}


        {isLoading && (

          <div className="message assistant">

            <div className="message-content">

              <div className="source-badge">
                AI Agent
              </div>

              Thinking...

            </div>

          </div>

        )}

      </div>


      <form
        onSubmit={sendMessage}
        className="input-form"
      >

        <input
          type="text"
          value={input}
          onChange={(e) =>
            setInput(e.target.value)
          }
          placeholder="Ask about crop prices, arrivals, weather, or mandi concepts..."
          disabled={isLoading}
        />


        <button
          type="submit"
          disabled={
            isLoading ||
            !input.trim()
          }
        >
          {isLoading ? "..." : "Send"}
        </button>

      </form>

    </div>

  );
}


export default App;