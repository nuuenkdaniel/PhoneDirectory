let html = "";
$(document).ready(function() {
    $("#filterOptions").on("change",function() {
        html = "";
        if(document.querySelector("#name-filter").checked) {
            html += '<div id="name-field">\
            <label for="name">Name*</label>\
            <input id="name" type="text" class="form-control" placeholder="Enter a name" required>\
            </div>';
        }
        else if(document.getElement) {
            document.getElementById("name-field").remove();
        }

        if(document.querySelector("#email-filter").checked) {
            html += '<div id="email-field">\
            <label for="email">Email*</label>\
            <input id="email" type="email" class="form-control" placeholder="Enter an email" required>\
            </div>'
        }
        else if(document.getElementById("email-field") !== null) {
            document.getElementById("email-field").remove();
        }
        
        if(document.querySelector("#number-filter").checked) {
            html += '<div id="number-field">\
            <label for="number">Phone Number*</label>\
            <input id="number" type="tel" class="form-control" placeholder="Enter a phone number" required>\
            </div>'
        }
        else if(document.getElementById("number-field") !== null) {
            document.getElementById("number-field").remove();
        }

        if(document.querySelector("#address-filter").checked) {
            html += '<div id="address-field">\
            <label for="street-address">Street Address*</label>\
            <input id="street-address" type="text" class="form-control" placeholder="Enter the street address" required>\
            <label for="city">City*</label>\
            <input id="city" type="text" class="form-control" placeholder="Enter the city" required>\
            <label for="state">State*</label>\
            <input id="state" type="text" class="form-control" placeholder="Enter the state" required>\
            <label for="zip">Zip*</label>\
            <input id="zip" type="number" class="form-control" placeholder="Enter the zipcode" required>\
            </div>'
        }
        else if(document.getElementById("address-field") !== null) {
            document.getElementById("address-field").remove();
        }

        document.getElementById("search-fields").innerHTML = html;
    });
});