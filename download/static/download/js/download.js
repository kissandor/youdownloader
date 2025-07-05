const filename = "Layouts.mp4";  // ezt dinamikusan is megadhatod
const checkUrl = `/check-status/${filename}/`;

const intervalId = setInterval(() => {
    fetch(checkUrl)
        .then(response => response.json())
        .then(data => {
            if (data.ready) {
                clearInterval(intervalId);
                document.getElementById("loader").style.display="none";
                document.getElementById("status").textContent = "File is ready to download from the below link: ";
                document.getElementById("download-link").href = `/media/downloads/${filename}`;
                document.getElementById("download-link").style.display = "inline-block";
            } else {
                document.getElementById("status").textContent = "Preparing for download...";
            }
        });
}, 5000); // 3 másodpercenként ellenőriz