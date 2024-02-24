import React, {useEffect, useState} from "react";

import './App.css'
import NewChatButton from "./components/NewChatButton";
import ChatHistory from "./components/ChatHistory";
import SaveChatHistoryButton from "./components/SaveChatHistoryButton"
import UserInputContainer from "./components/UserInputContainer";
import SignOutButton from "./components/SignOutButton";
import Footer from "./components/Footer";
import Logo from "./components/Logo";
import LiveChatFeed from "./components/LiveChatFeed";
import getCurrentChat from "./components/GetCurrentChat";
import getUserChatHistory from "./components/GetUserChatHistory"
import { Amplify } from 'aws-amplify';
import awsExports from './aws-exports';
import { withAuthenticator, useAuthenticator} from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

Amplify.configure(awsExports);

function App() {
    const { user, signOut } = useAuthenticator((context) => [context.user]);
    const [previousChats, setPreviousChats] = useState([])
    const [userInput, setUserInput] = useState("")
    const [currentChat, setCurrentChat] = useState([
        {
            "text": "Hello, I'm a chatbot which leverages the gpt-3.5-turbo model. But " +
                "the context for my responses comes from a semantic search performed against a vector database " +
                "of youtube video transcripts using your questions. Currently I can only answer questions on the videos from " +
                "a playlist of podcasts on personal finance and investing from the The Diary of a CEO channel.",
            "isBot": true
        }
    ])

    const userId = user.username
    useEffect(() => {
        getUserChatHistory({userId, previousChats, setPreviousChats});
    }, []);

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
                <SaveChatHistoryButton
                    userId={userId}
                    previousChats={previousChats}
                ></SaveChatHistoryButton>
                <SignOutButton
                    signOut={signOut}
                ></SignOutButton>
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

export default withAuthenticator(App);
