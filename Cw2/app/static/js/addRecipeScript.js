$.fn.AddIngrediant = function()
{
    $count = $("#ingrediants").children().length;

    if($count >= 20)
        return;

    $parent = $("#ingrediants").children().first().clone();
    $ingrediant = $parent.find('#ingrediant0')
    $quantity =  $parent.find('#quantity0')

    $ingrediant.val("");
    $quantity.val("");

    $ingrediant.attr("name", "ingrediants-" + $count +"-ingrediant")
    $quantity.attr("name", "ingrediants-" + $count +"-quantity")

    $parent.appendTo("#ingrediants");
}

$.fn.RemoveIngrediant = function()
{
    $count = $("#ingrediants").children().length;

    if($count <= 1)
        return;
    
    $("#ingrediants").children().last().remove();
}

$("#AddIngrediantsButton").click(function(e)
{
    e.stopImmediatePropagation();
    $(this).AddIngrediant();
});

$("#RemoveIngrediantsButton").click(function(e)
{
    e.stopImmediatePropagation();
    $(this).RemoveIngrediant();
});