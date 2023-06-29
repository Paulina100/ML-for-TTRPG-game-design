export function renderHeader(headerText) {
    return (
        <h1 className="content-header">
            {headerText}
        </h1>
    );
}

export function displaySubmitInfo(submitButtonId, formId) {
    const submitButton = document.getElementById(submitButtonId);
    submitButton.setAttribute("style", "display: none");

    let form = document.getElementById(formId);
    const submittedMessage = document.createElement("p");
    submittedMessage.setAttribute("class", "message");
    submittedMessage.appendChild(document.createTextNode("Submit successful"));
    form.appendChild(submittedMessage);

    setTimeout(() => {
        form.removeChild(submittedMessage);
        submitButton.setAttribute("style", "display: block");
    }, 1250);
}
