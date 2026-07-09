const chat = document.getElementById("chat");
const textarea = document.getElementById("question");
const button = document.getElementById("sendButton");

button.addEventListener("click", sendMessage);

textarea.addEventListener("keydown", function(e){
    if(e.key==="Enter" && !e.shiftKey){
        e.preventDefault();
        sendMessage();
    }
});

function addMessage(role, text){
    const div = document.createElement("div");
    div.className = "message " + role;
    div.innerHTML = text.replace(/\n/g,"<br>");
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    return div;
}

async function sendMessage(){
    const question = textarea.value.trim();
    if(question==="")
        return;
    addMessage("user", question);
    textarea.value="";
    button.disabled=true;
    const thinking = addMessage(
        "assistant",
        "<i>Thinking...</i>"
    );
    try{
        const response = await fetch("/chat",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                question:question
            })
        });
        const data = await response.json();
        let html = data.answer;
        if(data.sources && data.sources.length){
            html += "<hr>";
            html += "<strong>Sources</strong><br>";
            data.sources.forEach(source=>{
                html += "📄 " + source + "<br>";
            });
        }
        thinking.innerHTML = html.replace(/\n/g,"<br>");
    }
    catch(error){
        thinking.innerHTML =
            "<span style='color:red'>Connection error.</span>";
    }
    button.disabled=false;
}