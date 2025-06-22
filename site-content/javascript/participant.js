
async function submitParticipantData(){
    /*
    Fetch participant data from website and post it to 
    the backend. So far no data managment e.g:. dateofbirth is 
    in dd.mm.yyyy format but it is not checked if the format is met.
    */
    let paidInt = document.getElementById("paid").checked ? 1 : 0;
    const params = new URLSearchParams({
        "participantID" : document.getElementById("id").value,
        "lastname" : document.getElementById("lastname").value,
        "firstname" : document.getElementById("firstname").value,
        "club" : document.getElementById("club").value,
        "dateofbirth" : document.getElementById("dateofbirth").value,
        "gender" : document.getElementById("gender").value,
        "nation" : document.getElementById("nation").value,
        "paid" : paidInt,
        "note" : document.getElementById("note").value
    })
    fetch(window.domain + "/participants/update?" + params.toString(),{
    method: "POST"
    })
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => console.error("Error", err));
}

async function fetchParticipantData(id){
/*
Fetches participant data from the backend server and writes
the content in the respective location.
*/

    const response = await fetch(window.domain + "/participants/participant/" + id);
    const data = await response.json();
    document.getElementById("id").value=data["fencerID"];
    document.getElementById("lastname").value=data["lastname"] ;
    document.getElementById("firstname").value =data["firstname"] ;
    document.getElementById("club").value = data["club"];
    document.getElementById("dateofbirth").value = data["dateofbirth"];
    document.getElementById("gender").value = data["gender"];
    document.getElementById("nation").value = data["nation"];
    if (data["paid"] == 1) {
      document.getElementById("paid").checked = true;  
    }
    if (data["adult"] == 1) {
      document.getElementById("adult").checked = true;  
    }
    document.getElementById("note").value = data["note"]

    const table = document.getElementById("signups");
    for (let tournament of Object.values(data["participation"])){
        let row = document.createElement("tr");
        let tdname = document.createElement("td")
        tdname.textContent = tournament[1]
        let tdcheck = document.createElement("td");
        let check = document.createElement("input");
        check.type="checkbox";

        row.appendChild(tdname);
        row.appendChild(tdcheck);
        tdcheck.appendChild(check);
        /*
        tournament participation is tracked via check box. On change the
        database will be updated to the respective value.
        */
        if (tournament[2]==1){check.checked = true;}
        check.addEventListener("change", function() {
            let checkedInt = check.checked ? 1 : 0;
            const params= new URLSearchParams({
                "participantId" : data["fencerID"],
                "signuplistID" : tournament[0],
                "boolInt" : checkedInt 
            })

        fetch(window.domain + "/signups/signParticipantUp?" + params.toString(),{
            method: "POST"
        })
        .then(res => res.json())
        .then(data => console.log(data))
        .catch(err => console.error("Error", err));

        }) 
        table.appendChild(row);
    }
}


async function deleteParticipant(){
    /*
    Removes a participant and all associated data from the 
    database. This will also remove the respective particpant
    from all other databases!
    May need a check that this is not possible if the participant
    is active in any tournament.
    */
    const params = new URLSearchParams({
        "participantID" : document.getElementById("id").value,
    })
    fetch(window.domain + "/participants/delete?" + params.toString(),{
    method: "POST"
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        window.close()
        })
    .catch(err => console.error("Error", err));
}