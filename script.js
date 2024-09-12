let source = "./event/";
let page = 1;
const perPage = 50;
let loading = false;


function categoryChanged() {
    var category = document.getElementById("category").value;
    // Call your function with the selected category
    // For example:
    if (category === "all") {
      buildZone.innerHTML = ''; // clear buildZone
      page = 1;
      loadEvents('get_data');
    } else if (category === "sink") {
      page = 1;
      buildZone.innerHTML = ''; // clear buildZone
      loadEvents('get_data_by_region/1');
    } else if (category === "stove-top") {
      page = 1;
      buildZone.innerHTML = ''; // clear buildZone
      loadEvents('get_data_by_region/2');
    }
}

// function to show image when we click on a image
function showImage(imageSrc) {
    let popupImage = document.getElementById("popupImage");
    popupImage.src = imageSrc;
    
    let imagePopup = document.getElementById("imagePopup");
    imagePopup.style.display = "block";
    document.body.style.overflow = "hidden";
}
    // function to hide the image when we click on cross button
function closeImage() {
    let imagePopup = document.getElementById("imagePopup");
    imagePopup.style.display = "none";
    document.body.style.overflow = "auto";
 }

function createEvent(folder) {
    const eventDiv = document.createElement('div');
    eventDiv.classList.add('event');
    eventDiv.innerHTML =   
                            '<img class="item" src="'+ source + folder +'/before.png" alt="">' +
                            '<img class="item" src="'+ source + folder +'/after.png" alt="">' +
                            '<img class="item" src="'+ source + folder +'/hour1.png" alt="">' +
                            '<img class="item" src="'+ source + folder +'/hour6.png" alt="">' +
                            '<img class="item" src="'+ source + folder +'/hour12.png" alt="">' +
                            '<img class="item" src="'+ source + folder +'/hour24.png" alt="">' +
                            '<video class="item" controls loop>' +
                            '<source src="' + source + folder +'/video.mp4" type="video/mp4" />' +
                            '</video>'
                            ;
    return eventDiv;
}

const buildZone = document.getElementById('build');
function loadEvents(callType) {
    

    fetch('http://192.168.1.6:5000/' + callType )
        .then(response => response.json())
        .then(data => {
            
            data.forEach(folder => {
                const div = createEvent(folder[0]);
                console.log(div);
                buildZone.appendChild(div);
            });
        })
        .catch(error => console.error(error));
}

function pageChange() {
    page = document.getElementById("page-number").value;
    loadMore();
}

function loadMore() {
  if (loading) {
    return;
  }
  var category = document.getElementById("category").value;


    loading = true;
    if (category === "all") {
        fetch(`http://192.168.1.6:5000/get_data_for_pages/${page}/${perPage}`)
        .then(response => response.json())
        .then(data => {
            data.forEach(folder => {
            const div = createEvent(folder[0]);
            buildZone = div;
            });
            page++;
            loading = false;
        })
        .catch(error => console.error(error));
    } else {
        if (category === "sink") {
            region=1;
        } else if (category === "stove-top") {
            region=2;
        }
        fetch(`http://192.168.1.6:5000/get_data_for_pages_with_regions/${page}/${perPage}/${region}`)
        .then(response => response.json())
        .then(data => {
            data.forEach(folder => {
            const div = createEvent(folder[0]);
            buildZone = div;
            });
            page++;
            loading = false;
        })
        .catch(error => console.error(error));
    }
    loading = false;
    document.getElementById("page").textContent = page;
}

loadEvents('get_data');