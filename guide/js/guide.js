var send_data = {}

$(document).ready(function () {
    // reset all parameters on page load
    resetFilters();
    // bring all the data without any filters
    getAPIData();
    // get commodity types
    // AJAX call into commodity type select options
    getType();

    // on selecting the country option
    $("#commodity_type").on('change', function () {
        // since commodity_code_system is dependent
        // on commodity type select, empty all the options from select input
        $("#commodity_code_system").val("all");
        $("#commodity_code").val("all");
        send_data['commodity_code_system'] = '';
        send_data['commodity_code'] = '';

        // update the selected type
        if(this.value == "all")
            send_data['commodity_type'] = "";
        else
            send_data['commodity_type'] = this.value;

        //get commodity coding systems of selected type
        getCodeSystem(this.value);
        // get api data of updated filters
        getAPIData();
    });

    $("#commodity_code_system").on('change', function() {
        send_data['commodity_code'] = '';
        $("#commodity_code").val("all");
        if(this.value == "all")
            send_data['commodity_code_system'] = "";
        else
            send_data['commodity_code_system'] = this.value;
        var str = $("#commodity_type").val();
        getCode(this.value, str);
        getAPIData();
    });

    $("#commodity_code").on('change', function() {
        if(this.value == "all")
            send_data['commodity_code'] = "";
        else
            send_data['commodity_code'] = this.value;
        getAPIData();
    });

    // display the results after reseting the filters
    $("#display_all").click(function(){
        resetFilters();
        getAPIData();
    })
})


/**
    Function that resets all the filters
**/
function resetFilters() {
    $("#commodity_type").val("all");
    $("#commodity_code_system").val("all");
    $("#commodity_code").val("all");

    //clearing up the code select box
    getCode("all");
    // check if getCode SYstem should be rest

    send_data['commodity_type'] = '';
    send_data['commodity_code_system'] = '';
    send_data['commodity_code'] = '';
    send_data['format'] = 'json';
}


function getAPIData() {
    let url = $('#list_data').attr("url")
    $.ajax({
        method: 'GET',
        url: url,
        data: send_data,
        beforeSend: function(){
            $("#no_results h5").html("Loading data...");
        },
        success: function (result) {
            console.log('success');
        },
        error: function (response) {
            $("#no_results h5").html("Something went wrong");
            $("#list_data").hide();
        }
    });
}


function getType() {
    let url = $("#commodity_type").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            type_options = "<option value='all' selected>Select Commodity Type</option>";
            $.each(result["commodity_type"], function (a, b) {
                type_options += "<option>" + b + "</option>"
            });
            $("#commodity_type").html(type_options)
        },
        error: function(response){
            console.log(response);
        }
    });
}


function getCodeSystem(commodity_type) {
    let url = $("#commodity_code_system").attr("url");
    let code_system_options = "<option value='all' selected>Select Code System</option>";
    $.ajax({
        method: 'GET',
        url: url,
        data: {
            "commodity_type": commodity_type
        },
        success: function (result) {
            $.each(result["commodity_code_system"], function(a, b) {
                commodity_code_system_options += "<option>" + b + "</option>"
            });
            $("#commodity_code_system").html(commodity_code_system_options)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getCode(commodity_code_system, commodity_type) {
    let url = $("#commodity_code").attr("url");
    let code_option = "<option value='all' selected>Select Code</option>";
    $.ajax({
        method: 'GET',
        url: url,
        data: {
            "commodity_code_system": commodity_code_system,
            "commodity_type": commodity_type
        },
        success: function (result) {
            $.each(result["commodity_code"], function (a, b) {
                commodity_code_option += "<option>" + b + "</option>"
            });
            $("#commodity_code").html(commodity_code_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}
