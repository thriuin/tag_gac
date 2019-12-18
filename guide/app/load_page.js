
var surveyJSON = {
    title: "Trade Agreements, Single Implementation Guideline", pages: [
        {
            name: "page1", questions: [
                {type: "text", inputType: "number", name: "contractValue", title: "Estimated Value", isRequired: true},
                {
                    type: "html",
                    name: "cv_info",
                    html: "Estimate the maximum total value of the procurement over its entire duration."
                },
                {
                    type: "dropdown",
                    name: "department",
                    title: "Organization",
                    isRequired: true,
                    colCount: 0,
                    choices: [
                        "Treasury Board of Canada",
                        "Privy Council Office"
                    ]
                },
                {type: "html", name: "org_info", html: "Select the organization that you are purchasing on behalf of."},
                {
                    type: "dropdown",
                    name: "commodity_type",
                    title: "Commodity Type",
                    isRequired: true,
                    colCount: 0,
                    choices: [
                        "Goods",
                        "Services",
                        "Construction"
                    ]
                },
                {
                    type: "html",
                    name: "ct_info",
                    html: "Select whether the procurement is a Goods, Service, or Construction."
                },
                {
                    type: "dropdown",
                    name: "goods_code",
                    title: "Commodity Code",
                    isRequired: true,
                    visibleIf: "{commodity_type} = 'Goods'",
                    choicesByUrl: {
                        url: "http://127.0.0.1:8000/goods/?format=json",
                        valueName: "fs_code_desc"
                    }
                },
                {
                    type: "dropdown",
                    name: "service_code",
                    title: "Commodity Code",
                    isRequired: true,
                    visibleIf: "{commodity_type} = 'Services'",
                    choicesByUrl: {
                        url: "http://127.0.0.1:8000/services/?format=json",
                        valueName: "desc_en"
                    }
                },
                {
                    type: "dropdown",
                    name: "construction_code",
                    title: "Commodity Code",
                    isRequired: true,
                    visibleIf: "{commodity_type} = 'Construction'",
                    choicesByUrl: {
                        url: "http://127.0.0.1:8000/construction/?format=json",
                        valueName: "fs_code_desc"
                    }
                },
                {
                    type: "dropdown",
                    name: "solicitation_procedure",
                    title: "Solicitation Procedure",
                    isRequired: true,
                    colCount: 0,
                    choices: [
                        'Traditional Competitive',
                        'Open Bidding',
                        'Sole Source']
                },
            ]
        },
        {
            name: "page2", questions: [
                {
                    type: "html",
                    name: "ctexinfo",
                    html: "<h2>Exceptions</h2>"
                },
                {
                    type: "checkbox",
                    choices:  custom_questions,
                    isRequired: false,
                    name: "exceptions",
                    title: "Check all exceptions that apply"
                }]
        },
        {
            name: "page3", questions: [
                {
                    type: "checkbox",
                    choicesByUrl: {
                        url: "http://127.0.0.1:8000/tendering_reasons",
                        valueName: "desc_en"
                    },
                    isRequired: false,
                    name: "exceptions",
                    title: "Limited Tendering Reasons"
                }
            ]
        },
        {
            name: "page4", questions: [
                {
                    type: "checkbox",
                    choices:  cfta_questions,
                    isRequired: false,
                    name: "cfta_exceptions",
                    title: "CFTA Exceptions"
                }
            ]
        }
    ]
};

Survey.StylesManager.applyTheme("bootstrap");

var survey = new Survey.Model(surveyJSON);
new Vue({el: '#surveyContainer', data: {survey: survey}});

