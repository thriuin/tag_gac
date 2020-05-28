// Place this file in static/js/
var send_data = {}

$(document).ready(function () {
    // reset all parameters on page load
    // bring all the data without any filters
    // get commodity types
    // AJAX call into commodity type select options
    getType();

    // on selecting the country option

    $("#type").on('change', function() {
        send_data['code'] = '';
        $("#code").val("all");
        if(this.value == "all")
            send_data['type'] = "";
        else
            send_data['type'] = this.value;
        getCode(this.value);
    });

    $("#code").on('change', function() {
        if(this.value == "all")
            send_data['code'] = "";
        else
            send_data['code'] = this.value;
    });
})


/**
    Function that resets all the filters
**/
function resetFilters() {
    $("#type").val("all");
    $("#code").val("all");

    //clearing up the code select box
    getCode("all");

    send_data['type'] = '';
    send_data['code'] = '';
    send_data['format'] = 'json';
}



function getType() {
    let url = $("#type").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            type_options = "<option value='all' selected>Select Commodity Type</option>";
            $.each(result["type"], function (a, b) {
                type_options += "<option>" + b + "</option>"
            });
            $("#type").html(type_options)
        },
        error: function(response){
            console.log(response);
        }
    });
}


function getCode(type) {
    let url = $("#code").attr("url");
    let code_option = "<option value='all' selected>Select Code</option>";
    $.ajax({
        method: 'GET',
        url: url,
        data: {
            "type": type
        },
        success: function (result) {
            $.each(result["code"], function (a, b) {
                code_option += "<option>" + b + "</option>"
            });
            $("#code").html(code_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}



