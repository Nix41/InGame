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
    let filter = document.getElementById("name_filter");
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
    let filter = document.getElementById("gender_filter");
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
    app.launch = app.games_dic[id].launch;
    app.score = app.games_dic[id].score;
    app.size = app.games_dic[id].size;
    app.language = app.games_dic[id].language;
    app.gamemode = app.games_dic[id].game_mode;
    app.category = app.games_dic[id].category;
}

function filter_over(gen){
    if(app.filter_key != ''){
        $("#" + app.filter_key).css("background-color","rgb(77,77,77)");
        $("#" + app.filter_key).css("margin","5px");
        $("#" + app.filter_key).css("border-radius","15px");
        $("#" + app.filter_key).css("width","100px");
        app.on_mouse[app.filter_key] = 0;
    }
    app.filter_key = gen.id;
    if(gen.id != "Todos"){
        $("#" + gen.id).css("background-color","");
        $("#" + gen.id).css("margin","0px");
        $("#" + gen.id).css("border-radius","0px");
        $("#" + gen.id).css("width","110px");
        app.on_mouse[gen.id] = 1;
        app.filter_key = gen.id;
    }
}

function filter_mouse(id,x){
    if(app.filter_key != id.id){
        if(x == 1){
            $('#'+ id.id).css('background-color','rgb(209,4,4)')
        }else{
            $('#'+ id.id).css('background-color','rgb(77,77,77)')
        }
    }
}

function filter_subgen_mouse(id,x){
        if(x == 1){
            $('#'+ id).css('background-color','rgb(209,4,4)')
        }else{
            $('#'+ id).css('background-color','rgb(51,51,51)')
        }
}



