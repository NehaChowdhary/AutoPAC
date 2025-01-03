import { useState } from "react";

import Message from "./components/Message";
import Input from "./components/Input";
import History from "./components/History";
import Clear from "./components/Clear";

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import "./App.css";
import axios from "axios";

export default function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);

  const handleSubmit = async () => {
    // console.log(messages);
    setMessages((messages) => [
      ...messages,
      {
          role: "user",
          content: input // Assuming 'answer' is the property you want to render
      }
    ]);

    try{
        const res = await axios.post("http://10.5.20.125:5000/get_answer", {"question":input},{
            headers: {
              "Access-Control-Allow-Origin": "*"
            },
        },{
          timeout: 60000, // Set a timeout of 1 minute
        });
        console.log(res)
        if (res.status==200) {
          try {
              const answer = res.data.answer;
              console.log(answer); // Logging the response for debugging purposes
      
              // Update messages state
              setMessages((messages) => [
                  ...messages,
                  {
                      role: "assistant",
                      content: answer // Assuming 'answer' is the property you want to render
                  }
              ]);
      
              // Update history state
              setHistory((history) => [
                  ...history,
                  { question: input, answer: answer } // Assuming 'answer' is the property you want to store
              ]);
          } catch (error) {
              toast.error("Failed to parse data fetched from server");            
          }
      } else {
          throw new Error("Error fetching data from server!");
      }
    }
    catch(error){
      console.log(error);
      toast.error("Failed to fetch data from server"); 
    }
    
  };

  const clear = () => {
    setMessages([]);
    setHistory([]);
  };

  return (
    <div className="App">
      <div className="Column">
        <h3 className="Title">PrivateGPT for Open Policy Agent Queries</h3>
        <div className="Content">
          {messages.map((el, i) => {
            return <Message key={i} role={el.role} content={el.content} />;
          })}
        </div>
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onClick={input ? handleSubmit : undefined}
        />
      </div>
      <div className="Column">
        <h3 className="Title">History</h3>
        <div className="Content">
          {history.map((el, i) => {
            return (
              <History
                key={i}
                question={el.question}
                onClick={() =>
                  setMessages([
                    { role: "user", content: history[i].question },
                    { role: "assistant", content: history[i].answer }
                  ])
                }
              />
            );
          })}
        </div>
        <Clear onClick={clear} />
        <ToastContainer />
      </div>
    </div>
  );
}
