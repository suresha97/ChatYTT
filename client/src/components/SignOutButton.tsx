import React from "react";
import {chatItem} from "./LiveChatFeed";
import signOutImg from "../assets/icons8-sign-out-50.png"

interface Props {
    signOut: any
}


function SignOutButton({signOut}: Props) {
    return (
        <button
            className="sign-out-button"
            onClick={signOut}
        > <img className="sign-out-img" src={signOutImg}/> Sign Out
        </button>
    )
}

export default SignOutButton
