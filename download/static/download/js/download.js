const filename = "Layouts.mp4";  // ezt dinamikusan is megadhatod
const checkUrl = `/check-status/${filename}/`;

const intervalId = setInterval(() => {
    fetch(checkUrl)
        .then(response => response.json())
        .then(data => {
            if (data.ready) {
                clearInterval(intervalId);
                document.getElementById("status").textContent = "Letöltés kész!";
                document.getElementById("download-link").href = `/media/downloads/${filename}`;
                document.getElementById("download-link").style.display = "inline-block";
            } else {
                document.getElementById("status").textContent = "Készül a videó...";
            }
        });
}, 3000); // 3 másodpercenként ellenőriz