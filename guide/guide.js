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
    $("#commodity_type_en").on('change', function () {
        // since commodity_code_system is dependent
        // on commodity type select, empty all the options from select input
        $("#commodity_code_system_en").val("all");
        $("#commodity_code_en").val("all");
        send_data['commodity_code_system_en'] = '';
        send_data['commodity_code_en'] = '';

        // update the selected type
        if(this.value == "all")
            send_data['commodity_type_en'] = "";
        else
            send_data['commodity_type_en'] = this.value;

        //get commodity coding systems of selected type
        getCodeSystem(this.value);
        // get api data of updated filters
        getAPIData();
    });

    $("#commodity_code_system_en").on('change', function() {
        send_data['commodity_code_en'] = '';
        $("#commodity_code_en").val("all");
        if(this.value == "all")
            send_data['commodity_code_system_en'] = "";
        else
            send_data['commodity_code_system_en'] = this.value;
        var str = $("#commodity_type_en").val();
        getCode(this.value, str);
        getAPIData();
    });

    $("#commodity_code_en").on('change', function() {
        if(this.value == "all")
            send_data['commodity_code_en'] = "";
        else
            send_data['commodity_code_en'] = this.value;
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
    $("#commodity_type_en").val("all");
    $("#commodity_code_system_en").val("all");
    $("#commodity_code_en").val("all");

    //clearing up the code select box
    getCode("all");
    // check if getCode SYstem should be rest

    send_data['commodity_type_en'] = '';
    send_data['commodity_code_system_en'] = '';
    send_data['commodity_code_en'] = '';
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
    let url = $("#commodity_type_en").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            type_options = "<option value='all' selected>Select Commodity Type</option>";
            $.each(result["commodity_type_en"], function (a, b) {
                type_options += "<option>" + b + "</option>"
            });
            $("#commodity_type_en").html(type_options)
        },
        error: function(response){
            console.log(response);
        }
    });
}


function getCodeSystem(commodity_type_en) {
    let url = $("#commodity_code_system_en").attr("url");
    let commodity_code_system_options = "<option value='all' selected>Select Code System</option>";
    $.ajax({
        method: 'GET',
        url: url,
        data: {
            "commodity_type_en": commodity_type_en
        },
        success: function (result) {
            $.each(result["commodity_code_system_en"], function(a, b) {
                commodity_code_system_options += "<option>" + b + "</option>"
            });
            $("#commodity_code_system_en").html(commodity_code_system_options)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getCode(commodity_code_system_en, commodity_type_en) {
    let url = $("#commodity_code_en").attr("url");
    let commodity_code_option = "<option value='all' selected>Select Code</option>";
    $.ajax({
        method: 'GET',
        url: url,
        data: {
            "commodity_code_system_en": commodity_code_system_en,
            "commodity_type_en": commodity_type_en
        },
        success: function (result) {
            $.each(result["commodity_code_en"], function (a, b) {
                commodity_code_option += "<option>" + b + "</option>"
            });
            $("#commodity_code_en").html(commodity_code_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}
