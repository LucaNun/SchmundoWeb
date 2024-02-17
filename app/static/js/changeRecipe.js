var valuelist = {}
var ingredientlist = {}
var steplist = {}

$(document).on("keyup", ".testinput", function() {
  var group = $(this).data("group");
  if (group == "value") {
    valuelist[this.name] = this.value;
  }else if (group == "ingredient") {
    ingredientlist[this.name] = this.value;
  } else if (group == "step"){
    steplist[this.name] = this.value;    
  }
  
});


$(document).on("click", ".sendButton", function() {
  var id = $("#recipeID").data("id")
  $.ajax({
    url: 'http://127.0.0.1:5000/recipe/change/'+id,
    type: 'POST',
    data: JSON.stringify({"valueliste": valuelist, "ingredientlist": ingredientlist, "steplist": steplist}),
    contentType: 'application/json',
    dataType: 'json'
  });
});