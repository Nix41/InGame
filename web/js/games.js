async function get_games(){
    let value = await eel.filter_games()();
    let i = 1;
    let list = [];
    for (x in value) {
        Vue.set(app.games_dic, x, value[x]);
        if(i%5 == 0){
            list.push(value[x]);
            app.games.push(list);
            list = [];
        }else{
            list.push(value[x]);
        }
        key = "id" + i;
        i++;
    }
    app.games.push(list);
}
async function filter_games_by_name(){
    app.games = []
    let filter = document.getElementById('name_filter');
    let value = await eel.filter_games(filter.value)();
    let i = 1;
    let list = [];
    for (x in value) {
        if(i%5 == 0){
            list.push(value[x]);
            app.games.push(list);
            list = [];
        }else{
            list.push(value[x]);
        }
        i++;
    }
    app.games.push(list);
}
async function filter_games_by_gender(){
    app.games = []
    let filter = document.getElementById('gender_filter');
    let value = await eel.filter_games(gender=filter.value)();
    for (x in value) {
        app.games.push(value[x]);
    }
}

function see(id){
    app.name = app.games_dic[id].name;
    app.description = app.games_dic[id].description;
    app.requirements = app.games_dic[id].requirements;
    app.genders = app.games_dic[id].genders;
    app.key = id;
}

