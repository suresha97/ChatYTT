import React, {useState} from "react";
import {chatItem} from "./LiveChatFeed";
import saveIcon from "../assets/saveicon.png"
import tickIcon from "../assets/tickicon.png"


interface Props {
    userId: String
    previousChats: Array<Array<chatItem>>
}

function SaveChatHistoryButton({userId, previousChats}: Props){
    const [isChatSaved, setIsChatSaved] = useState(false)

    const saveChatHistory = () => {
        const options = {
            method: 'PUT',
            headers: {
                "Content-Type": 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                "userId": userId,
                "chatHistory": previousChats
            })
        }


        fetch(`${import.meta.env.VITE_ENDPOINT}save-chat-history/`, options).then(
            (response) => response.json()
        ).then(
            (data) => {
                setIsChatSaved(true)
            }
        )
    }

    return (
        <button
            className="save-chat-history-button"
            onClick={() => {saveChatHistory()}}
        > <img className={isChatSaved?"tick-icon-img":"save-icon-img"} src={isChatSaved?tickIcon:saveIcon}/>
        {isChatSaved?"Chats Saved":"Save Chat History"}
        </button>
    )
}

export default SaveChatHistoryButton
