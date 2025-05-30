async function fetchTournaments(url) {
    const response = await fetch(url);
    if (!response.ok) {
        console.log("failed to fetch tournaments")
    }
    const data = await response.json();
    const list = document.getElementById("tournamentlist")
    if (data.length==0) {
        const window = document.getElementById("mainwindow");
        const pele = document.createElement("p");
        pele.textContent("There exist no tournaments so far.");
        window.appendChild(pele);
    }
    else {
        for (const [key,value] of Object.entries(data)) {
            const li = document.createElement("li");
            const ref = document.createElement("a");
            ref.href = "tour/" + key;
            ref.textContent = value;
            li.appendChild(ref) ;
            list.appendChild(li);
            }
    }
}