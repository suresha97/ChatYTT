import chatgptlogo from "../assets/chatgptlogo.svg";
import youtubelogo from "../assets/youtubelogo.svg";


function Logo() {
    return (
        <div id="logo">
            <img id="img-chatgpt" src={chatgptlogo}/>
            <img id="img-youtube" src={youtubelogo}/>
            <div id="logo-text">Chat with Youtube</div>
        </div>
    )
}

export default Logo
