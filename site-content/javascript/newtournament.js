
window.onload = function() {

if (window.sessionStorage.tname) {
    document.getElementById('tournament_name').value = window.sessionStorage.tname;
}

if (window.sessionStorage.tmode) {
    document.getElementById('mode_select').value = window.sessionStorage.tmode;
}
else {
    document.getElementById('mode_select').value="ko";
    window.sessionStorage.tmode="ko";
}

if (window.sessionStorage.precount) {
    document.getElementById('pre_select').value = window.sessionStorage.precount;
}
else {
        window.sessionStorage.precount = 1
}

}


/* On user induced change of group count and size reavaluate the other. */
async function reCalcCount() {
    let total_text = document.getElementById("p_count");

    let group_s_text = document.getElementById("group_s");
    let group_c_text = document.getElementById("group_c");

    
    window.sessionStorage.gsize=document.getElementById("group_s").value;
    window.sessionStorage.gcount=Math.ceil( parseInt(total_text.value)  / parseInt(group_s_text.value))

    group_c_text.value = window.sessionStorage.gcount;

}

async function reCalcSize() {
    let total_text = document.getElementById("p_count");

    let group_s_text = document.getElementById("group_s");
    let group_c_text = document.getElementById("group_c");


        
    window.sessionStorage.gsize=Math.ceil( parseInt(total_text.value)  / parseInt(group_c_text.value))
    window.sessionStorage.gcount=document.getElementById("group_c").value;

    group_s_text.value = window.sessionStorage.gsize;

}


async function updateTotal() {
    window.sessionStorage.liststr = "";

    const container=document.getElementById("tour_list");
    const checkboxes = container.querySelectorAll(".vBox");

    const total_text = document.getElementById("p_count")


    checkboxes.forEach(checkbox => {
        if (checkbox.checked){
            window.sessionStorage.liststr += checkbox.getAttribute('data-value') + "_";
        }

    })
    const response = await fetch(window.domain + "/signup_overlap/" + window.sessionStorage.liststr)
    if (!response.ok){
        console.log("Signup total failed from: " + url)
    }
    const data = await response.json()
    
    window.sessionStorage.ptotal = data[0]
    total_text.value = data[0]

    let group_s_text = document.getElementById("group_s");
    let group_c_text = document.getElementById("group_c");
    let submit_button = document.getElementById("submit");


    if (total_text.value== "0") {
        group_c_text.setAttribute('disabled', '');
        group_s_text.setAttribute('disabled', '');
        submit_button.setAttribute('disabled', '')
        group_s_text.value= "-";
        group_c_text.value= "-";
        window.sessionStorage.gsize = 0;
        window.sessionStorage.gcount = 0;

    }
    else {
        group_c_text.removeAttribute('disabled');
        group_s_text.removeAttribute('disabled');
        submit_button.removeAttribute('disabled');
        window.sessionStorage.gsize = Math.min(6,Math.floor(Math.sqrt(parseInt(total_text.value))));
        group_s_text.value=window.sessionStorage.gsize;
        window.sessionStorage.gcount =Math.ceil( parseInt(total_text.value)  / parseInt(group_s_text.value));
        group_c_text.value = window.sessionStorage.gcount;
    }
}


/*
fetch elements from the signup list with number of registrations.
Then extend the table by a row for each signuplist.
*/
async function signuplists(url) {
    const response = await fetch(url);
    if (!response.ok) {
        console.log("failed to fetch from " & url);
    }
    const data = await response.json();
    for (const [key,value] of Object.entries(data)) {
            const li = document.createElement("tr");
            const  tdn = document.createElement("td");
            const  tdp = document.createElement("td");
            const  tdc = document.createElement("td");
            tdn.textContent = value[1];
            tdp.textContent = value[2];
            const include_box = document.createElement("input");
            include_box.type = "checkbox";
            include_box.name = "Include";
            include_box.value = 0;
            include_box.className = "vBox";
            include_box.dataset.value = value[0] ;
            include_box.addEventListener('change', updateTotal)
            tdc.appendChild(include_box);
            li.appendChild(tdn);
            li.appendChild(tdp);
            li.appendChild(tdc);
            const list = document.getElementById("tour_list");
            list.appendChild(li)
    }

}

async function loadGroupSetup(url=window.domain + "/signup_overlap_particpants/" + window.sessionStorage.liststr) {
    let gframe = document.getElementById("groups_frame")
    gframe.innerHTML="";

    const response = await fetch(url);
    const data = await response.json();

    let groupsdiv = document.createElement("div");
    let inner_div = document.createElement("div");
    let inner = document.createElement("p");

    groupsdiv.id="groups_unsorted";
    inner.textContent="Unassigned Participants:";
    groupsdiv.appendChild(inner);
    groupsdiv.appendChild(inner_div);
    gframe.appendChild(groupsdiv);

    
    groupsdiv.addEventListener("dragover", function (e) {
        e.preventDefault(); // Must prevent default to allow drop
    });
    groupsdiv.addEventListener("drop", function (e) {
        e.preventDefault();
        const id = e.dataTransfer.getData("text/plain");
        const draggedElement = document.getElementById(id);
        inner_div.appendChild(draggedElement);
    });


    /*
    Add drag elements to unassigned participants;
    */
   for (const [key,fencer_data] of Object.entries(data)) {
        let drag_ele = document.createElement("div");
        drag_ele.id= "drag_fencer"+ fencer_data[2];
        drag_ele.className = "drag_fencer";
        drag_ele.draggable =true;
        drag_ele.FencerId= fencer_data[2];
        drag_ele.addEventListener("dragstart", function (e) {
            e.dataTransfer.setData("text/plain", drag_ele.id);
        });

        let drag_ele_inner = document.createElement("p");
        drag_ele_inner.style="margin: 0px";
        drag_ele_inner.textContent=
                fencer_data[0] + "\n " +
                fencer_data[1] + "\n" + 
                fencer_data[1]
                ;
        drag_ele.appendChild(drag_ele_inner);
        inner_div.appendChild(drag_ele);
    };

    groupsdiv = document.createElement("div");

    groupsdiv.id="groups_group";
    gframe.appendChild(groupsdiv);
    for (let i =1; i<= window.sessionStorage.gcount; i++) {
        let groupdiv = document.createElement("div");
        groupdiv.className="group";
        groupdiv.id="group"+i;
        inner = document.createElement("p");

        inner.textContent="Group "+i;
        groupdiv.appendChild(inner);
        groupsdiv.appendChild(groupdiv);

        for (let j = 1; j<= window.sessionStorage.gsize; j++){
            let part_drop_zone = document.createElement("div");
            part_drop_zone.id = "participant_"+i+"_"+j;
            part_drop_zone.className="dropzone";
            part_drop_zone.addEventListener("dragover", function (e) {
                e.preventDefault(); // Must prevent default to allow drop
            });
            part_drop_zone.addEventListener("drop", function (e) {
                e.preventDefault();
                
                // Only allow drop if the drop zone is empty
                if (part_drop_zone.children.length === 0) {
                    const id = e.dataTransfer.getData("text/plain");
                    const draggedElement = document.getElementById(id);
                    part_drop_zone.appendChild(draggedElement);
                } else {
                    const id = e.dataTransfer.getData("text/plain");
                    const draggedElement = document.getElementById(id);
                    const replaceElement = part_drop_zone.children[0];
                    const oldParent = draggedElement.parentElement;

                    oldParent.appendChild(replaceElement);
                    part_drop_zone.appendChild(draggedElement);
                }
            });
            part_drop_zone.textContent = "Fencer" + j ;
            groupdiv.appendChild(part_drop_zone);
        }
    }
}

async function sendData() {
    if (window.sessionStorage.tname &&
        window.sessionStorage.gcount &&
        window.sessionStorage.gsize &&
        window.sessionStorage.liststr &&
        window.sessionStorage.tmode
    ) {
    try {
        await fetch(window.domain + "/submitTournament",
        {
            mode: 'no-cors',
            method: "POST",
            headers: {
            "Content-type": "application/json",
            },
            body: JSON.stringify(
                {
                    tname: "123"
                }
            )
        })
        }
    catch (error) {
            console.error("Error sending data:", error);
        }
    }
    else {
        alert("Not all form fields are filled.")
    }
}

async function sendData1() {
            body: JSON.stringify(
                {
                    tname: window.sessionStorage.tname,
                    gcount: window.sessionStorage.gcount,
                    gsize: window.sessionStorage.gsize,
                    liststr: window.sessionStorage.liststr,
                    tmode: window.sessionStorage.tmode
                }
            )
}
