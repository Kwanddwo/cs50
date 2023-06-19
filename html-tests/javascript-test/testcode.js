try {
    const correctbutton = document.querySelector("#button-2");
    const falsebuttons = document.querySelectorAll("#button-1, #button-3, #button-4, #button-5");
    const result = document.querySelector("#buttonresult");
    done = false;


    function correct() {
        if (!done) {
        result.innerHTML = "Correct!";
        }
        done = true
    }

    function incorrect() {
        if (!done) {
        result.innerHTML = "Incorrect";
        }
        done = true;
    }


    correctbutton.addEventListener("click", correct);
    for (let fbutton of falsebuttons)
    {
        fbutton.addEventListener("click", incorrect);
    }

}
catch (error) {
    console.error(error);
}