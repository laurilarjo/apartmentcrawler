var apartmentData = [];

$(document).ready(function() {

    /**
     * Parse the json file
     * For this to work, you need to allow file access in Chrome:
     * /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --allow-file-access-from-files
     */
    $.getJSON("file://localhost/Users/larkki/Documents/code/apartmentscraper/scraped_data.json", function(data) {

        console.log("json parsing starts");
        jQuery.each(data, function() {
            console.log("row parsing starts");

            //we need the numbers, so skip these apartments
            if (this.price == undefined ||
                this.monthly_costs == undefined ||
                this.construction_year == undefined ||
                this.surface_area == undefined) {
                return true;
            }

            //prepare the data
            this.price = Larkki.convertToNumber(this.price);
            this.monthly_costs = Larkki.convertToNumber(this.monthly_costs);
            this.surface_area = Larkki.convertToNumber(this.surface_area);

            //make calculation
            this.price_per_square = this.price / this.surface_area;
            this.estimated_rent = this.surface_area * 10;
            this.yearly_profit = 12 * this.estimated_rent - 12 * this.monthly_costs;
            this.roi = this.yearly_profit / this.price * 100;

            //nicer display
            this.price_per_square = Math.round(this.price_per_square*100)/100;
            this.yearly_profit = Math.round(this.yearly_profit*100)/100;
            this.roi = Math.round(this.roi*100)/100;

            apartmentData.push(this);
            console.log(this);
        });

        console.log("json parsing ends");
        console.log(apartmentData)

        //convert the stuff to array
        var tabledata = [];
        jQuery.each(apartmentData, function() {
            var arr = [];
            arr.push(this.url);
            //arr.push(this.address);
            arr.push(this.location);
            arr.push(this.construction_year);
            arr.push(this.surface_area);
            arr.push(this.monthly_costs);
            arr.push(this.price);
            arr.push(this.price_per_square);
            arr.push(this.estimated_rent);
            arr.push(this.yearly_profit);
            arr.push(this.roi);
            tabledata.push(arr);
        });
        console.log(tabledata);

        //Display the stuff in jquery-datatable
        $('#demo').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="example"></table>' );
        $('#example').dataTable( {
            "aaData": tabledata,
            "aoColumns": [
                { "sTitle": "Url" ,
                    "fnRender": function(obj) {
                    var sReturn = obj.aData[ obj.iDataColumn ];
                    return "<a href=" + sReturn + ">" + sReturn + "</a>";
                }},
                //{ "sTitle": "Address" },
                { "sTitle": "Location" },
                { "sTitle": "Construction_year", "sClass": "center" },
                { "sTitle": "Surface_area", "sClass": "center" },
                { "sTitle": "monthly_costs", "sClass": "center" },
                { "sTitle": "price", "sClass": "center" },
                { "sTitle": "price_per_square", "sClass": "center" },
                { "sTitle": "estimated_rent", "sClass": "center" },
                { "sTitle": "yearly_profit", "sClass": "center" },
                { "sTitle": "roi", "sClass": "center" }
            ]
        } );
    });

});

var Larkki = {
    convertToNumber: function(someString) {
        if (someString != undefined) {
            someString = someString.replace(/,/g, '.'); //replace , with .
            return someString.replace(/[^\d.]/g, ''); //strip off all but numbers
        }
    }
}