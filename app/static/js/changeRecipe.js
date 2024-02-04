var valuelist = []

$(document).on("keyup", ".testinput", function() {
    console.log(this.name, this.value);
    valuelist.push({this.name, this.value}); //Need a fix
    console.log(valuelist)
    console.log(JSON.stringify(valuelist))
  });


$(document).on("click", ".sendButton", function() {
  console.log(valuelist)
  console.log(JSON.stringify(valuelist))
  $.ajax({
    url: 'http://127.0.0.1:5000/recipe/ajax',
    type: 'POST',
    data: JSON.stringify(valuelist),
    contentType: 'application/json',
    dataType: 'json',
    success: function(response) {
        console.log(response);
        console.log("funkt");
    },
    error: function(error) {
        console.log(error);
        console.log("funkt nicht");
    }
  });
});