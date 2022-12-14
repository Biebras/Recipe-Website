$.fn.setDeffaultPassword = function()
{
    $password = $("#password").children();
    $confirmPassword = $("#confirmPassword").children();

    $ingrediant.val("");
    $quantity.val("");

    $ingrediant.attr("name", "ingrediants-" + $count +"-ingrediant")
    $quantity.attr("name", "ingrediants-" + $count +"-quantity")

    $parent.appendTo("#ingrediants");
}