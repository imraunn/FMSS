$(".extra-fields-customer").click(function () {
  $(".customer_records").clone().appendTo(".customer_records_dynamic");
  $(".customer_records_dynamic .customer_records").addClass("single remove");
  $(".single .extra-fields-customer").remove();
  $(".single").append(
    '<a href="#" class="remove-field btn-remove-customer">Remove Fields</a>'
  );
  $(".customer_records_dynamic > .single").attr("class", "remove");

  $(".customer_records_dynamic input").each(function () {
    var count = 0;
    var fieldname = $(this).attr("name");
    $(this).attr("name", fieldname + count);
    count++;
  });
});

$(document).on("click", ".remove-field", function (e) {
  $(this).parent(".remove").remove();
  e.preventDefault();
});
