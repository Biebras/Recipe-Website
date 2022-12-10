$.fn.AddIngrediant = function()
{
    $clone = $("#ingrediants").children().first().clone();
    $clone.val("");
    $clone.appendTo("#ingrediants");
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

$("#submitButton").click(function(e)
{
    
});