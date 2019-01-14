$(document).ready(function () {

    // javascript for the semantic ui dropdown
    $('.ui.dropdown').dropdown({
        onChange: function (value, text, $selectedItem) {
            // console.log(value);
        },
        forceSelection: false,
        selectOnKeydown: true,
        showOnFocus: true,
        on: "hover"
    });

    // ajax setup for the csrf error
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    $('#clearValues').click(function () {
        $('.ui.dropdown').dropdown("clear");
    });

    // ajax for search
    $("#search-params").submit(function (event) {

        event.preventDefault();
        $("#loader").show()
        var url = "/reviews/dashboard";

        var data = {};
        data["cuisines"] = $("input[name=cuisines-text]").val();
        data["categories"] = $("input[name=categories-text]").val();
        data["establishments"] = $("input[name=establishments-text]").val();
        data["query"] = $("input[name=query]").val();

        var t = "";
        $.ajax({
            url: url,
            type: "POST",
            data: data,
            success: function (res) {
                res = JSON.parse(res);
                res["restaurants"].forEach(function (data) {
                    // console.log(data.restaurant.name);
                    let thumb = data.restaurant.thumb;
                    if (!thumb) {
                        thumb = "https://images.pexels.com/photos/920220/pexels-photo-920220.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940";
                    }
                    const restaurantId = data.restaurant.id;
                    const restaurantName = data.restaurant.name;
                    const restaurantLocation = data.restaurant.location.locality;
                    const restaurantRating = data.restaurant.user_rating.aggregate_rating;
                    const restaurantCuisines = data.restaurant.cuisines;
                    const restaurantUrl = data.restaurant.url;
                    const restaurantRatingColor = data.restaurant.user_rating.rating_color;
                    t += `<div class="item">
                            <div class="image">
                                <img src="${thumb}">
                            </div>
                            <div class="content">
                                <a class="header" href="/reviews/place/${restaurantId}">
                                    ${restaurantName}
                                </a>
                                <div class="meta">
                                  <div class="meta">  <span class="cinema">${restaurantLocation}</span>
                                </div>
                                <div class="description">
                                    <p>
                                    </p>
                                </div>
                                    <div class="extra">
                                        <div 
                                            class="ui right floated primary button"
                                            onclick="window.open('${restaurantUrl}')">
                                            Visit the zomato page
                                            <i class="right chevron icon"></i>
                                        </div>
                                        <div class="ui label" style="background:#${restaurantRatingColor}">
                                            <i class="star icon"></i> ${restaurantRating}
                                        </div>
                                    </div>
                                    <div class="ui label"><i class="globe icon"></i> ${restaurantCuisines}</div>
                                </div>
                            </div>
                        </div>`;
                });
                console.log(t);
                $("#right-pane").html(t);
            },
            error: function () {
                console.log("error");
            }
        })

    });

    $('.ui.rating')
        .rating({
            initialRating: 0,
            maxRating: 5
        })
        ;

    $("#review-form").submit(function (event) {

        event.preventDefault();
        

        var data = {};
        data["res_id"] = $("input[name=res_id]").val();
        data["review_text"] = $("#review_text").val();
        data["rating"] = $(".ui.rating").rating('get rating');
        data["username"] = $("input[name=username]").val();
        console.log(data)
        
        var url = "/reviews/place/" + data['res_id'];

        var s = "";
        $.ajax({
            url: url,
            type: "POST",
            data: data,
            success: function (res) {
                s = `<div class="comment">
            <a class="avatar">
                <img src="https://www.pmidpi.com/wp-content/uploads/2015/07/person-placeholder.jpg">
            </a>
            <div class="content">
                <a class="author">${ data.username }</a>
                <div class="metadata">
                <div class="rating">
                    <i class="star icon"></i>
                    ${ data.rating } stars
                </div>
            </div>
            <div class="text">
              ${ data.review_text }
            </div>
        </div>`;
        $(".ui.comments").append(s);
        $(".ui.rating").rating('clear rating');
        $("#review_text").val("");
            },
            error: function () {
                console.log("error");
            }
        })

    });
});