const chatbotToggler = document.querySelector(".chatbot-toggler");
const minimiseBtn = document.querySelector(".minimise-btn");
const expandBtn = document.querySelector(".expand-btn");
const chatbox = document.querySelector(".chatbox");
const expanded = document.querySelector(".expanded-chatbot");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".send-btn");

const modalContainer = document.querySelector(".modal-container");
const closeModalBtn = document.querySelector(".btn-close");
const overlay = document.querySelector(".overlay");
const modal = document.getElementById("zoom-checkbox")

const terminateBtn = document.querySelector(".terminate-btn");

// Fetch clicked image as modal
const getModal = (src) => {
    const newImage = document.createElement("img");
    newImage.setAttribute("src", src);
    newImage.classList.add("modal-img");
    modal.append(newImage);
    modalContainer.classList.remove("hidden");
}

// Add click event listeners to allow any image to open in modal
const addImgEvents = (msg) => {
    const imgs = msg.querySelectorAll(".chat-img");
    imgs.forEach((img) => {
        img.addEventListener("click", (e) => {
            getModal(e.target.src);
        });
    })
}

// Fetch existing chat history upon page reload
const getChatHistory = () => {
    const requestOptions = {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    }
    fetch("/chat_history", requestOptions).then(res => res.json()).then(data => {
        let chatHistory = data['history'];
        chatHistory.forEach(msg => {
            chatbox.appendChild(createChatLi(msg['question'], 'outgoing'));
            chatbox.appendChild(createChatLi(msg['answer'], 'incoming'));
        })
    });
}

getChatHistory();

const openFeedbackBox = (feedbackType) => {
    // Create darkened background overlay
    const popupOverlay = document.createElement("div");
    popupOverlay.classList.add("feedback-popup-overlay", "overlay");
    chatbox.appendChild(popupOverlay);

    // Create feedback comment box with close button
    const popupBox = document.createElement("div");
    let prompt = "<textarea rows='4' placeholder='What did you like about this response?'></textarea> \
                  <label class='feedback-checkbox'> \
                      <input type='checkbox' name='checkbox' value='solved'/> \
                      My problem was solved \
                  </label> \
                  <label class='feedback-checkbox'> \
                      <input type='checkbox' name='checkbox' value='accurate'/> \
                      The information was accurate \
                  </label> \
                  <label class='feedback-checkbox'> \
                      <input type='checkbox' name='checkbox' value='fast'/> \
                      The response time was fast \
                  </label>"
    if (feedbackType == "negative") {
        prompt = "<textarea rows='4' placeholder='How could this response be improved?'></textarea>"
    }
    popupBox.classList.add("feedback-popup-box");
    let closeBtn = document.createElement("span");
    closeBtn.className = "material-symbols-outlined close";
    closeBtn.innerHTML = "close";
    popupBox.appendChild(closeBtn);
    popupBox.innerHTML += "<h4>Provide additional feedback</h4>";
    chatbox.appendChild(popupBox);

    // Create form with comment textarea
    const form = document.createElement("form");
    popupBox.appendChild(form);
    const textarea = document.createElement("textarea");
    textarea.setAttribute("name", "comment");
    textarea.setAttribute("rows", "4");
    if (feedbackType == "positive") {
        textarea.setAttribute("placeholder", "What did you like about this response?");
    } else {
        textarea.setAttribute("placeholder", "How could this response be improved?");
    }
    form.appendChild(textarea);

    // Add star ratings
    const ratingsContainer = document.createElement("div");
    ratingsContainer.classList.add("ratings-container");
    for (let i = 0; i < 5; i++) {
        let radio = document.createElement("input");
        radio.setAttribute("type", "radio");
        radio.setAttribute("name", "rating");
        radio.setAttribute("value", 5 - i);
        radio.setAttribute("id", "rating-" + (5 - i));

        let label = document.createElement("label");
        label.setAttribute("for", "rating-" + (5 - i));
        let star = document.createElement("span");
        star.classList.add("material-symbols-sharp", "star");
        star.innerHTML = "&#xe838";
        label.appendChild(star);
        
        ratingsContainer.appendChild(radio);
        ratingsContainer.appendChild(label);
    }
    form.appendChild(ratingsContainer);

    // Add base checklists and alter content according to feedback type
    const feedbackCheckbox1 = document.createElement("label");
    feedbackCheckbox1.classList.add("feedback-checkbox");
    const checkbox1 = document.createElement("input");
    checkbox1.setAttribute("type", "checkbox");
    checkbox1.setAttribute("name", "feedback");
    feedbackCheckbox1.appendChild(checkbox1);
        
    const feedbackCheckbox2 = document.createElement("label");
    feedbackCheckbox2.classList.add("feedback-checkbox");
    const checkbox2 = document.createElement("input");
    checkbox2.setAttribute("type", "checkbox");
    checkbox2.setAttribute("name", "feedback");
    feedbackCheckbox2.appendChild(checkbox2);

    if (feedbackType == "positive") {
        // Add checklist for question solved and accuracy for positive feedback
        checkbox1.setAttribute("value", "solved");
        checkbox2.setAttribute("value", "accurate");
        feedbackCheckbox1.innerHTML += "My problem was solved";
        feedbackCheckbox2.innerHTML += "The information was accurate";
        form.appendChild(feedbackCheckbox1);
        form.appendChild(feedbackCheckbox2);

    } else {
        // Add checklist for question unresolved and inaccuracy for negative feedback
        checkbox1.setAttribute("value", "unsolved");
        checkbox2.setAttribute("value", "inaccurate");
        feedbackCheckbox1.innerHTML += "My problem wasn't solved";
        feedbackCheckbox2.innerHTML += "The information was inaccurate";
        form.appendChild(feedbackCheckbox1);
        form.appendChild(feedbackCheckbox2);
    }

    // Add submit button
    const submitBtn = document.createElement("input");
    submitBtn.setAttribute("type", "submit");
    submitBtn.setAttribute("value", "Submit");
    form.appendChild(submitBtn);
    submitBtn.addEventListener("click", (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        formData.append("feedbackType", feedbackType);
        fetch('/feedback', {
            method: 'POST',
            body: formData
        });
        popupOverlay.remove();
        popupBox.remove();
    });

    // Close feedback box on click
    closeBtn = document.querySelector("span.material-symbols-outlined.close");
    closeBtn.addEventListener("click", () => {
        const formData = new FormData(form);
        formData.append("feedbackType", feedbackType);
        fetch('/feedback', {
            method: 'POST',
            body: formData
        });
        popupOverlay.remove();
        popupBox.remove();
    });
    popupOverlay.addEventListener("click", () => {
        const formData = new FormData(form);
        formData.append("feedbackType", feedbackType);
        fetch('/feedback', {
            method: 'POST',
            body: formData
        });
        popupOverlay.remove();
        popupBox.remove();
    });
}

// Create thumbs up/thumbs down basic feedback buttons for each message
const createFeedbackButtons = (chatElement) => {
    const feedbackContainer = document.createElement("div");
    feedbackContainer.classList.add("feedback-container");
    
    // Add thumbs up button
    const thumbUp = document.createElement("button");
    thumbUp.classList.add("thumbs-button");
    thumbUp.innerHTML = "<span class='material-symbols-rounded'>thumb_up</span>"
    thumbUp.addEventListener("click", () => {
        thumbUp.querySelector(".material-symbols-rounded").classList.toggle("clicked");
        openFeedbackBox("positive");
        thumbUp.disabled = true;
        thumbDown.remove();
    });
    feedbackContainer.appendChild(thumbUp);

    // Add thumbs down button
    const thumbDown = document.createElement("button");
    thumbDown.classList.add("thumbs-button");
    thumbDown.innerHTML = "<span class='material-symbols-rounded'>thumb_down</span>"
    thumbDown.addEventListener("click", () => {
        thumbDown.querySelector(".material-symbols-rounded").classList.toggle("clicked");
        openFeedbackBox("negative");
        thumbDown.disabled = true;
        thumbUp.remove();
    });
    feedbackContainer.appendChild(thumbDown);
    chatElement.appendChild(feedbackContainer);
}

const removePreviousFeedback = () => {
    let feedbackContainers = document.querySelectorAll(".feedback-container");
    if (feedbackContainers.length > 1) {
        const latestFeedback = feedbackContainers[feedbackContainers.length - 2];
        if (!latestFeedback.querySelector(".thumbs-button").disabled) {
            latestFeedback.remove();
        }
    }
}

let userMessage = null; // Variable to store user's message
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
    // Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").innerHTML = message;
    addImgEvents(chatLi);
    return chatLi; // return chat <li> element
}

const typingAnimation = () => {
    // Create a chat <li> element with blinking typing animation
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", "incoming");
    let chatContent = `<span class="material-symbols-outlined">smart_toy</span><p class="typing"><span></span><span></span><span></span></p>`;
    chatLi.innerHTML = chatContent;
    return chatLi; // return chat <li> element
}

const scrollChat = () => {
    if(window.location.pathname === "/expand"){
        expanded.scrollTo(0, expanded.scrollHeight);
    }else{
        chatbox.scrollTo(0, chatbox.scrollHeight);
    }
}

const generateResponse = (chatElement) => {
    const API_URL = "/api/chatbot";
    const messageElement = chatElement.querySelector("p");

    // Define the properties and message for the API request
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: userMessage
        })
    }

    // Send POST request to API, get response and set the reponse as paragraph text
    fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
        messageElement.innerHTML = data['response_message'];
        messageElement.classList.remove("typing");
        addImgEvents(messageElement);
        createFeedbackButtons(chatElement);
        removePreviousFeedback();
    }).catch(() => {
        messageElement.classList.add("error");
        messageElement.textContent = "Oops! Something went wrong. Please try again.";
    }).finally(() => {
        scrollChat();
    });
}

const handleChat = () => {
    userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
    if(!userMessage) return;

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the user's message to the chatbox
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    scrollChat();
    
    // Display typing animation while waiting for the response
    const incomingChatLi = typingAnimation();
    chatbox.appendChild(incomingChatLi);
    scrollChat();
    generateResponse(incomingChatLi);
}

chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window 
    // width is greater than 800px, handle the chat
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

// Close image modal
const closeModal = () => {
    modalContainer.classList.add("hidden");
    const modalImg = document.querySelector(".modal-img");
    modalImg.remove();
}

// Close image modal if escape key is pressed
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !modalContainer.classList.contains("hidden")) {
      closeModal();
    }
});

// Close chat session
terminateBtn.addEventListener("click", () => {
    const userConfirmed = window.confirm("Are you sure you want to terminate the chat?");

    if (userConfirmed) {
        // Send an HTTP GET request to the '/close' endpoint in your Flask application
        fetch('/close', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json', // Set headers as needed
            },
        })
            .then(response => {
                if (response.ok) {
                    document.body.classList.remove("show-chatbot");
                    location.reload();
                } else {
                    console.error('Request failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});

closeModalBtn.addEventListener("click", closeModal);
overlay.addEventListener("click", closeModal);
sendChatBtn.addEventListener("click", handleChat);
minimiseBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
expandBtn.addEventListener("click", () => window.open('expand', '_blank').focus());
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));