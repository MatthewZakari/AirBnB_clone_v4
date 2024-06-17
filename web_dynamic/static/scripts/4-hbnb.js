const HOST = "0.0.0.0";

$(document).ready(function () {
  const amenities = {};

  """Event listener for amenity checkbox changes"""
  $("#input#check_amen").change(function () {
    const amenityName = $(this).attr("data-name");
    const amenityId = $(this).attr("data-id");

    """Add or remove amenities from the amenities object based on checkbox status"""
    if ($(this).is(":checked")) {
      amenities[amenityName] = amenityId;
    } else {
      delete amenities[amenityName];
    }

    """Update the displayed list of selected amenities"""
    const amenityNames = Object.keys(amenities);
    $(".amenities h4").text(amenityNames.sort().join(", "));
  });

  """Check API status and fetch places"""
  checkApiStatus();
  fetchPlacesWithAmenities();
});

"""Function to check the status of the API"""
function checkApiStatus() {
  const apiUrl = "http://0.0.0.0:5001/api/v1/status/";
  $.get(apiUrl, function (data, status) {
    """Update the API status indicator based on the response"""
    if (data.status === "OK" && status === "success") {
      $("#api_status").addClass("available");
    } else {
      $("#api_status").removeClass("available");
    }
  });
}

"""Function to fetch places based on selected amenities"""
function fetchPlacesWithAmenities() {
  const PLACES_URL = `http://${HOST}:5001/api/v1/places_search/`;
  $.ajax({
    url: PLACES_URL,
    type: "POST",
    headers: { "Content-Type": "application/json" },
    data: JSON.stringify({ amenities: Object.values(amenities) }),
    success: function (response) {
      """Clear the current list of places"""
      $("SECTION.places").empty();

      """Append each place to the places section"""
      response.forEach(place => {
        const article = `
          <article>
            <div class="title_box">
              <h2>${place.name}</h2>
              <div class="price_by_night">$${place.price_by_night}</div>
            </div>
            <div class="information">
              <div class="max_guest">${place.max_guest} Guest(s)</div>
              <div class="number_rooms">${place.number_rooms} Bedroom(s)</div>
              <div class="number_bathrooms">${place.number_bathrooms} Bathroom(s)</div>
            </div>
            <div class="description">
              ${place.description}
            </div>
          </article>`;
        $("SECTION.places").append(article);
      });
    },
    error: function (error) {
      console.error(error);
    }
  });
}
