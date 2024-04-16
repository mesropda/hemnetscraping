
try {
    var jsonDataScript = document.getElementById("json_data");
    var listings = JSON.parse(jsonDataScript.textContent);
    console.log(listings[0]);
    var databaseType = document.getElementById("databaseType");
    var dataType = JSON.parse(databaseType.textContent);
}

catch (error) {
    console.log("No jso file sent from backend");
}


let address = document.querySelector("#address");
let maxfee = document.querySelector("#maxfee");
let minrooms = document.querySelector("#minrooms");
let maxrooms = document.querySelector("#maxrooms");
let minarea = document.querySelector("#minarea");
let maxarea = document.querySelector("#maxarea");
let resultsDiv = document.querySelector("#results-div");
let showAvergae = document.querySelector("#show-avergae");
let fetchButton = document.querySelector("#fetch-button");
let startDate = document.querySelector("#start-date");
let endDate = document.querySelector("#end-date");

let popUpContainer = document.querySelector("#popup-container")
let contactUs = document.querySelectorAll("#contactus-btn");
let privacy = document.querySelectorAll('#privacy-btn')
let xBtn = document.querySelectorAll(".x-btn");
let box = document.getElementById("box");

let contactAtive = false
let privacyActive = false

contactUs[0].addEventListener('click', opdenHideContactUs);
contactUs[1].addEventListener('click', opdenHideContactUs);
privacy[0].addEventListener('click', opdenHidePrivacy);
privacy[1].addEventListener('click', opdenHidePrivacy);
privacy[2].addEventListener('click', opdenHidePrivacy);
window.addEventListener("resize", adjustBodyBeightforPopup)

fetchButton.addEventListener('click', showLoading); //Disable button while data is beeing downloaded


function showLoading() {
    fetchButton.textContent = "Fatching, please wait...";
    setTimeout(function () {
        fetchButton.classList.add("frozen");
    });
}

function adjustBodyBeightforPopup() {

    var mediaQuery = window.matchMedia('(max-height: 820px)')
    if (contactAtive == true || privacyActive == true) {
        document.body.style.height = "100vh";
        if (mediaQuery.matches) {
            document.body.style.height = "100vh";
        }
    }

}


function opdenHideContactUs() {
    let contactUsPopUp = document.getElementById("contact-us");
    if (contactUsPopUp.style.display == '' || contactUsPopUp.style.display == 'none') {
        if (privacyActive == true) {
            opdenHidePrivacy();
        }
        contactAtive = true;
        adjustBodyBeightforPopup();
        popUpContainer.classList.add('active');
        contactUsPopUp.style.display = 'block';
        box.style.display = 'none';

    }
    else {
        document.body.style.height = "100vh";
        console.log(document.body.style.height)
        contactUsPopUp.style.display = 'none';
        contactAtive = false;
        popUpContainer.classList.remove('active');
        try { displayResults(listings); }
        catch (error) { }
        box.style.display = 'flex';

    }
}

function opdenHidePrivacy() {
    let privacyPopUp = document.getElementById("privacy");
    if (privacyPopUp.style.display == '' || privacyPopUp.style.display == 'none') {
        if (contactAtive == true) {
            opdenHideContactUs();
        }
        privacyActive = true;
        adjustBodyBeightforPopup();
        popUpContainer.classList.add('active');
        privacyPopUp.style.display = 'block';
        box.style.display = 'none';

    }
    else {
        document.body.style.height = "100vh";
        privacyPopUp.style.display = 'none';
        privacyActive = false;
        popUpContainer.classList.remove('active');
        try { displayResults(listings); }
        catch (error) { }
        box.style.display = 'flex';

    }
}


let locations = [];
for (let listing of listings) {
    if (locations.includes(listing['address'])) { }
    else locations.push(listing['address']);
}

if (listings.length > 0) {
    let fetchedData = document.querySelector("#fetched-data");
    if (fetchedData.style.display === "" || fetchedData.style.display === "none") {
        fetchedData.style.display = "block";
    };

    let contentDiv = document.querySelector("#content-div");
    let filterCriterisText = document.querySelector("#filter-criteris-text");
    let filterButton = document.querySelector("#filter-button");
    contentDiv.classList.remove("inactive-div");
    filterCriterisText.classList.remove("inactive-div");
    filterButton.classList.remove("inactive-div");

    if (dataType['type'] == "sold") {
        let dateFilters = document.querySelectorAll('#filter-by-date');
        for (let dateFilter of dateFilters) {
            if (dateFilter.style.display === "" || dateFilter.style.display === "none") {
                dateFilter.style.display = "flex";
            };
        }
    };

}



address.addEventListener('keyup', (e) => {

    //Initially remove the old/previously enetered elements
    removeElements();
    //looping the listings addresses looking for matched names
    for (let location of locations) {
        //check if the listing's address startes with thhe enetered address
        if (location.toLocaleLowerCase().startsWith(address.value.toLocaleLowerCase()) && address.value !== '') {
            let listItem = document.createElement('li');
            listItem.classList.add('list-items');
            listItem.style.cursor = 'pointer';
            listItem.setAttribute('onclick', 'displayLocations("' + location + '")');
            //Display matched address
            let word = "<b>" + location.substr(0, address.value.length) + "</b>";
            word += location.substr(address.value.length);

            //diplay value in an array
            listItem.innerHTML = word;
            document.querySelector('.list').appendChild(listItem);
        }
    }
});

document.body.addEventListener('click', function (event) {
    if (event.target != address) {
        removeElements();
    }
});


function removeElements() {
    let items = document.querySelectorAll('.list-items');
    items.forEach((item) => {
        item.remove();
    });
}

function displayLocations(value) {
    address.value = value;
    removeElements();
};


function checkListing(listing) {
    if (address.value == "") { }
    else if (listing['address'].toLocaleLowerCase().includes(address.value.toLocaleLowerCase())) { }
    else return null;

    if (maxfee.value == "") { }
    else if (listing['monthlyFee'] <= parseInt(maxfee.value)) { }
    else return null;

    if (minrooms.value == "") { }
    else if (listing['roomNumber'] >= parseInt(minrooms.value)) { }
    else return null;

    if (maxrooms.value == "") { }
    else if (listing['roomNumber'] <= parseInt(maxrooms.value)) { }
    else return null;

    if (minarea.value == "") { }
    else if (listing['area'] >= parseInt(minarea.value)) { }
    else return null;

    if (maxarea.value == "") { }
    else if (listing['area'] <= parseInt(maxarea.value)) { }
    else return null;

    if (startDate.value == "") { }
    else if (new Date(listing['sell_date']) >= new Date((startDate.value))) { }
    else return null;

    if (endDate.value == "") { }
    else if (new Date(listing['sell_date']) >= new Date((endDate.value))) { }
    else return null;

    return listing;

}

function filter(listings) {
    filteredListings = [];
    total_price = 0;
    averge = 0;
    number_of_lisings = 0;

    for (let listing of listings) {

        //console.log(listing.address);
        let checked_listing = checkListing(listing);
        if (checked_listing !== null) {
            total_price += listing['price'];
            number_of_lisings += 1;
            filteredListings.push(listing);
        }
    }

    if (number_of_lisings >= 1) {
        averge = total_price / number_of_lisings;
    }

    return { 'averge-price': averge, 'number_of_lisings': number_of_lisings };
}

function displayResults(listings) {
    //let results_summary = document.createElement('DIV');
    average_price = 0;
    number_of_lisings = 0;

    if (address.value !== "" || maxfee.value !== "" || minrooms.value !== "" || maxrooms.value !== "" || minarea.value !== "" || maxarea.value !== "" || startDate.value !== "" || endDate.value !== 0) {

        results = filter(listings);
        average_price = results['averge-price'];
        number_of_lisings = results['number_of_lisings'];
    }
    else if (listings.length >= 1) {

        total_price = 0;
        for (let listing of listings) {
            if (listing['price'] !== '' || listing['price'] !== null) {
                total_price += listing['price'];
                number_of_lisings += 1;
            }
            average_price = total_price / number_of_lisings;
        }
    }

    average_price = parseInt(average_price);
    average_price = String(average_price);
    average_price = average_price.slice(0, -3) + " " + average_price.slice(-3);
    average_price = average_price.slice(0, -7) + " " + average_price.slice(-7);
    resultsDiv.innerHTML = `
        <p>The average price is: ${average_price} SEK<p> 
        The number of listings in the search: ${number_of_lisings}</p>
        `;
}

displayResults(listings);


showAvergae.addEventListener("click", function () {

    resultsDiv.innerHTML = "";
    displayResults(listings);

});
