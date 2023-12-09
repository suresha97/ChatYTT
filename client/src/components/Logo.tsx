import chatgpt from "../assets/chatgpt.svg";
import youtubelogo from "../assets/youtubelogo.svg";


function Logo() {
    return (
        <div>
            <div id="logo">
                <img id="img-chatgpt" src={chatgpt}/>
                <img id="img-youtube" src={youtubelogo}/>
            </div>
            <div id="logo-text">Chat with YouTube</div>
        </div>
    )
}

export default Logo
