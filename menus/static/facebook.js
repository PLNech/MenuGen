function share_meal(starter, main, desert, picture_url) {
    console.log("Sharing meal: ", starter, main, desert, picture_url);
    var caption = 'MenuGen me conseille ce repas : ' + starter + ', ' + main + ' et ' + desert + '.';
    var description = 'Et vous, que va-t\'il vous proposer ?';
    FB.ui({
            method: 'feed',
            name: 'Mon repas',
            picture: picture_url,
            description: description,
            caption: caption
        },
        function (response) {
        });
}
function share_recipe(name, picture_url) {
    console.log("Sharing recipe: ", name, picture_url);
    var caption = 'MenuGen me conseille cette recette : ' + name + '.';
    var description = 'Et vous, que va-t\'il vous proposer ?';
    var default_url = 'https://plnech.fr/files/menugen_logo.png';
    FB.ui({
            method: 'feed',
            name: 'Mon plat',
            description: description,
            picture: picture_url && picture_url != '' ? picture_url : default_url,
            caption: caption
        },
        function (response) {
        });
}
