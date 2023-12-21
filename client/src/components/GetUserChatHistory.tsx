import React from "react";
import {chatItem} from "./LiveChatFeed";

interface Props {
    userId: String
    previousChats: Array<Array<chatItem>>
    setPreviousChats: React.SetStateAction<any>
}

function getUserChatHistory({userId, previousChats, setPreviousChats}: Props){
    const options = {
            method: 'GET',
            headers: {
                "Content-Type": 'application/json',
                'Accept': 'application/json'
            }
        }
        console.log(userId)
        fetch(`${import.meta.env.VITE_ENDPOINT}get-chat-history/?userId=${userId}`, options).then(
            (response) => response.json()
        ).then(
            (data) => {
            if (data.response.chatHistory.length > 0) {
                setPreviousChats(
                        [
                            ...previousChats,
                            ...data.response.chatHistory
                        ]
                    )
                }
            }
        )
}

export default getUserChatHistory
