document.getElementById("predictionForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const data = {
        room_width: parseFloat(document.getElementById("room_width").value),
        room_height: parseFloat(document.getElementById("room_height").value),
        furniture_width: parseFloat(document.getElementById("furniture_width").value),
        furniture_height: parseFloat(document.getElementById("furniture_height").value),
        spacing: parseFloat(document.getElementById("spacing").value)
    };

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            document.getElementById("result").innerHTML = `<span style="color:red;">Error: ${result.error}</span>`;
        } else {
            document.getElementById("result").innerHTML = `X: ${result.x.toFixed(2)}, Y: ${result.y.toFixed(2)}`;
        }
    })
    .catch(error => console.error("Error:", error));
});
