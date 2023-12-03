import {useEffect, useRef} from "react";

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
                    <p>{item.text}</p>
                </div>
            })}
            <div ref={autoScrollToLoc}></div>
        </div>
    )
}

export default LiveChatFeed
