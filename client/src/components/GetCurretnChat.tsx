import React from "react";
import {chatItem} from "./LiveChatFeed";

interface Props {
    setCurrentChat: React.SetStateAction<any>
    userInput: string
    currentChat: Array<chatItem>
    setUserInput: React.SetStateAction<any>
}

function getCurrentChat({setCurrentChat, userInput, currentChat, setUserInput}: Props){
    const userInputText = userInput
    setUserInput("")
    setCurrentChat([
        ...currentChat,
        {
            "text": userInputText,
            isBot: false
        }
    ])

    const options = {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            query: userInputText,
            chatHistory: currentChat

        })
    }

    fetch("https://3dvunaz8l4.execute-api.eu-west-1.amazonaws.com/Prod/get-answer/", options).then(
        (response) => response.json()
    ).then(
        (data) => {
            setCurrentChat([
                ...currentChat,
                {
                    "text": userInputText,
                    "isBot": false
                },
                {
                    "text": data.response,
                    "isBot": true
                }
            ])
        }
    )
}

export default getCurrentChat
