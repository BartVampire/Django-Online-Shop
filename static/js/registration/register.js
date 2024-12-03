$(".close, .nope").on("click", function () {
  $(".modal").addClass("hidden");
  $(".open").addClass("active");
});

$(".open").on("click", function () {
  $(this).removeClass("active");
  $(".modal").removeClass("hidden");
});

