import {useEffect, useRef} from "react";
import chatgpt from "../assets/chatgpt.svg"
import userIcon from "../assets/usericonwhite.jpg"

export type chatItem = {
    text: string
    isBot: boolean
}

interface Props {
    currentChat: Array<chatItem>
}


function LiveChatFeed({currentChat}: Props) {
    const autoScrollToLoc = useRef(null)

    useEffect(() => {
        // @ts-ignore
        autoScrollToLoc.current.scrollIntoView()
    }, [currentChat])

    return (
        <div id="live-chat-feed">
            {currentChat.map((item, i) => {
                return <div key={i} className={item.isBot?"bot-chat-item":"user-chat-item"}>
                    <img className={item.isBot?"bot-chat-img":"user-chat-img"} src={item.isBot?chatgpt:userIcon}/>
                    <p>{item.text}</p>
                </div>
            })}
            <div ref={autoScrollToLoc}></div>
        </div>
    )
}

export default LiveChatFeed
