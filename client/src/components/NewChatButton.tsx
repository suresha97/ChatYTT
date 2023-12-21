import React from "react";
import {chatItem} from "./LiveChatFeed";
import addIcon from "../assets/add-30.png"

interface Props {
    setCurrentChat: React.SetStateAction<any>
    previousChats: Array<Array<chatItem>>
    setPreviousChats: React.SetStateAction<any>
    currentChat: Array<chatItem>
}


function NewChatButton({setCurrentChat, previousChats, setPreviousChats, currentChat}: Props) {
    const createNewChat = () => {
        setPreviousChats(
            [
                ...previousChats,
                currentChat
            ]
        )
        setCurrentChat([
            {
                "text": "Hello, I'm a chatbot which leverages the gpt-3.5-turbo model. But " +
                    "the context for my responses comes from a semantic search performed against a vector database " +
                    "of youtube video transcripts using your questions. Currently I can only answer questions on the videos from " +
                    "a playlist of podcasts on personal finance and investing from the The Diary of a CEO channel.",
                "isBot": true
            }
        ])
    }

    return (
        <button
            className="new-chat-button"
            onClick={() => {createNewChat()}}
        > <img className="add-icon-img" src={addIcon}/> New Chat
        </button>
    )
}

export default NewChatButton
