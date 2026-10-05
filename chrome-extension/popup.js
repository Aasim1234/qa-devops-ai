const questionBox = document.getElementById("question");
const answerBox = document.getElementById("answer");
const statusBox = document.getElementById("status");

const voiceBtn = document.getElementById("voiceBtn");
const askBtn = document.getElementById("askBtn");
const speakBtn = document.getElementById("speakBtn");


voiceBtn.addEventListener("click", () => {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        statusBox.textContent =
            "Speech recognition is not supported in this browser.";

        return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    statusBox.textContent = "Listening...";

    recognition.start();

    recognition.onresult = (event) => {

        const text =
            event.results[0][0].transcript;

        questionBox.value = text;

        statusBox.textContent =
            "Voice captured.";
    };

    recognition.onerror = (event) => {

        statusBox.textContent =
            "Voice error: " + event.error;
    };

    recognition.onend = () => {

        if (statusBox.textContent === "Listening...") {
            statusBox.textContent = "";
        }
    };
});


askBtn.addEventListener("click", async () => {

    const question =
        questionBox.value.trim();

    if (!question) {
        return;
    }

    statusBox.textContent =
        "Thinking...";

    answerBox.textContent = "";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data =
            await response.json();

        answerBox.textContent =
            data.answer || "No answer.";

        statusBox.textContent =
            "Done.";

    } catch (error) {

        statusBox.textContent =
            "Cannot connect to AI server.";

        answerBox.textContent =
            "Make sure the Python API is running.";
    }
});


speakBtn.addEventListener("click", () => {

    const answer =
        answerBox.textContent.trim();

    if (!answer) {
        return;
    }

    speechSynthesis.cancel();

    const speech =
        new SpeechSynthesisUtterance(answer);

    speech.lang = "en-IN";
    speech.rate = 0.95;

    speechSynthesis.speak(speech);
});