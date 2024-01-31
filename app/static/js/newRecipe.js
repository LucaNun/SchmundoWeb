let stepCounter = 1;

  function addNewField() {
    const newField = `
      <div class="form-group">
        <label for="step-${stepCounter}">Step ${stepCounter}:</label>
        <input type="text" class="form-control" id="step-${stepCounter}" name="step-${stepCounter}" placeholder="Beschreibung" required>
        <input type="number" id="step-duration-${stepCounter}" name="step-duration-${stepCounter}" placeholder="Dauer in Minuten" required>
      </div>
    `;

    $("#stepfields").append(newField);
    stepCounter++;
  }


  $(document).on("click", ".dropdown-item", function() {
    var headID = $(this).data("head");
    var id = $(this).data("id");
    var value = $(this).data("value");

    $("#"+headID).replaceWith(('<div class="btn btn-primary dropdown-toggle rounded-0 rounded-end" aria-expanded="false" data-bs-toggle="dropdown" id="'+ headID +'"><input type="text" id="'+ value +'"  name="'+ id +'" value="'+ value +'" hidden><label for="option1">'+ $(this).text() +'</label></div>'));
  });

  $(document).on("click", ".ingredient-btn", function() {
    name = this.innerText;
    id = $(this).data("id");
    $(document.getElementsByName("search")).val("");
    document.getElementById("ingredients-search").innerText = "";

    var template = $("#ingredients-template").clone();
    template.find(".form-control").attr("name", "ing-" + id);
    template.find(".input-group-text").attr("id", "Test").text(name);
    template.find(".dropdown-toggle").attr("id", "head-" + id).attr("data-id", id);
    template.find(".dropdown-item").attr("data-head", "head-" + id).attr("data-id", "ing-unit-" + id);
    $("#ingredients").append(template.html());
  });