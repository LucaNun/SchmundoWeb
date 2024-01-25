let fieldCounter = 1;

  function addNewField() {
    const newField = `
      <div class="form-group">
        <label for="field${fieldCounter}">Field ${fieldCounter}:</label>
        <input type="text" class="form-control" id="field${fieldCounter}" name="field${fieldCounter}">
      </div>
    `;

    $("#additional-fields").append(newField);
    fieldCounter++;
  }


  $(document).on("click", ".dropdown-item", function() {
    var headID = $(this).data("head");
    var value = $(this).data("value");

    $("#"+headID).replaceWith(('<div class="btn btn-primary dropdown-toggle rounded-0 rounded-end" aria-expanded="false" data-bs-toggle="dropdown" id="'+ headID +'"><input type="checkbox" id="'+ value +'" checked hidden><label for="option1">'+ $(this).text() +'</label></div>'));
  });

  $(document).on("click", ".ingredient-btn", function() {
    name = this.innerText;
    id = $(this).data("id");
    $(document.getElementsByName("search")).val("");
    document.getElementById("ingredients-search").innerText = "";

    var template = $("#ingredients-template").clone();
    template.find(".input-group-text").attr("id", "Test").text(name);
    template.find(".dropdown-toggle").attr("id", "head-" + id).attr("data-id", id);
    template.find(".dropdown-item").attr("data-head", "head-" + id);
    $("#ingredients").append(template.html());
  });