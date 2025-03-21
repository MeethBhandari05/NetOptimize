document.getElementById("tlbo-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch("/submit-tlbo", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Show response from backend
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
