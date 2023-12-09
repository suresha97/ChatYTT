import React from "react";
import {chatItem} from "./LiveChatFeed";
import messageIcon from "../assets/message.svg"

interface Props {
    previousChats: Array<Array<chatItem>>
    setCurrentChat: React.SetStateAction<any>
}

function ChatHistory({previousChats, setCurrentChat}: Props) {
    return (
        <div id="chat-history">
            {previousChats.map((chat, i) => {
                console.log(chat, chat.slice(1))
                if (previousChats.length != 0) {
                    return <button key={i} className="chat-history-button" onClick={() => setCurrentChat(chat)}>
                        <img className="chat-history-img" src={messageIcon}/>
                        {chat[1].text}
                    </button>
                }
            })}
        </div>
    )
}

export default ChatHistory
