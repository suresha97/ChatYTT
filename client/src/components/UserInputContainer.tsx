import React from "react";
import sendBtn from "../assets/send.svg"

interface Props {
    setUserInput: React.SetStateAction<any>
    userInput: string
    onClickEventHandler: React.MouseEventHandler<HTMLButtonElement>
}

function UserInputContainer({setUserInput, userInput, onClickEventHandler}: Props) {
    const getUserInput = (event: React.ChangeEvent<HTMLInputElement>) => {
        setUserInput(event.target.value)
    }

    // const handleEnterKey = (event: React.KeyboardEvent) => {
    //     console.log(event.key)
    //     if(event.key == "Enter") {
    //         onClickEventHandler
    //     }
    // }

    return (
        <div id="input-message-container">
            <input id="input-message" placeholder="Send Message" value={userInput} onChange={getUserInput}/>
            <button className="submit-message-button" onClick={onClickEventHandler}> <img className="submit-message-img" src={sendBtn} /> </button>
        </div>
    )
}

export default UserInputContainer
