import React, {useEffect, useState} from "react";

import './App.css'
import NewChatButton from "./components/NewChatButton";
import ChatHistory from "./components/ChatHistory";
import UserInputContainer from "./components/UserInputContainer";
import Footer from "./components/Footer";
import Logo from "./components/Logo";
import LiveChatFeed from "./components/LiveChatFeed";
import getCurrentChat from "./components/GetCurretnChat";


function App() {
    const [previousChats, setPreviousChats] = useState([])
    const [userInput, setUserInput] = useState("")
    const [currentChat, setCurrentChat] = useState([
        {
            "text": "Howdy, I'm a chatbot which leverages the gpt-3.5-turbo model. But " +
                "the context for my responses comes from a semantic search performed against a vector database " +
                "of youtube video transcripts using your questions. Currently I can only answer questions on the videos from " +
                "this here playlist: ",
            "isBot": true
        }
    ])

    const onClickEventHandler = () => {
        getCurrentChat(
            {setCurrentChat, userInput, currentChat, setUserInput}
        )
    }

    return <>
        <div id="app">
            <section id="chat-history-side-bar">
                <Logo></Logo>
                <NewChatButton
                    currentChat={currentChat}
                    setCurrentChat={setCurrentChat}
                    previousChats={previousChats}
                    setPreviousChats={setPreviousChats}
                ></NewChatButton>
                <ChatHistory
                    previousChats={previousChats}
                    setCurrentChat={setCurrentChat}
                ></ChatHistory>
            </section>
            <section id="main">
                <LiveChatFeed currentChat={currentChat}></LiveChatFeed>
                <UserInputContainer
                    userInput={userInput}
                    setUserInput={setUserInput}
                    onClickEventHandler={onClickEventHandler}
                ></UserInputContainer>
                <Footer></Footer>
            </section>
        </div>
    </>
}

export default App;
