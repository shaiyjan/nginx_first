async function fetchTournaments(url) {
    const response = await fetch(url);
    const list = document.getElementById("tournamentLinks");
    if (!response.ok) {
        console.log("failed to fetch tournaments");
        const li = document.createElement("li");
        li.textContent= "Not able to fetch tournaments."
        list.appendChild(li);
    }
    const data = await response.json();
    if (Object.entries(data).length == 0 ){
        const li = document.createElement("li");
        li.textContent= "No tournaments to fetch."
        list.appendChild(li);
    }
    console.log(response)
    for (const [key,tournament] of Object.entries(data)) {
        const li = document.createElement("li");
        const ref = document.createElement("a");
        ref.href = tournament["mode"] + "/" + tournament["id"];
        ref.textContent = tournament["name"];
        li.appendChild(ref) ;
        list.appendChild(li);
        console.log(key)
    }
    const create = document.createElement("a");
    create.href= "/newtournament.html";
    create.textContent= "Create new tournament";
    list.appendChild(document.createElement("li"))
    list.lastChild.appendChild(create);
}

async function fetchSignups(url) {
    const response = await fetch(url);
    console.log(response)
    if (!response.ok) {
        console.log("failed to fetch signups");
    }
    const data = await response.json();
    const list = document.getElementById("signupLinks");
    for (const [key,value] of Object.entries(data)) {
        const li = document.createElement("li");
        const ref = document.createElement("a");
        ref.href = "/signups/" + key;
        ref.textContent = value;
        li.appendChild(ref) ;
        list.appendChild(li);
    }
}