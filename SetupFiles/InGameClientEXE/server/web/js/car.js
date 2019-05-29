var check_del = 0;
var type = 0;

function car_g(x){
    if(x == 0){
        app.car_g = 0;
    }else{
        app.car_g = 1;
    }
}

function car_s(x){
    if(x == 0){
        app.car_s = 0;
    }else{
        app.car_s = 1;
    }
}

function car_f(x){
    if(x == 0){
        app.car_f = 0;
    }else{
        app.car_f = 1;
    }
}

async function get_car_games(){
    let value = await eel.get_games_cart()();
    let i = 1;
    app.games_dic = [];
    for (x in value) {
        app.games_dic.push([i-1, value[x]]);
        i++;
    }
}

async function get_car_series(){
    let value = await eel.get_series_cart()();
    let i = 1;
    type = 0;
    app.series_dic = [];
    for (x in value) {
        app.series_dic.push([i-1, value[x]]);
        i++;
    }
}

async function get_car_films(){
    let value = await eel.get_movies_cart()();
    let i = 1;
    type = 1;
    app.series_dic = [];
    for (x in value) {
        app.series_dic.push([i-1, value[x]]);
        i++;
    }
}

async function del_car_game(id){
    check_del = 1;
    var dic = [];
    let i = 1;
    for(x in app.games_dic){
        if(app.games_dic[x][1].id != id){
            dic.push([i-1,app.games_dic[x][1]]);
            i++;
        }
    }
    app.games_dic = dic;
    var new_list = [];
    for(x in app.games_dic){
        new_list.push([app.games_dic[x][1].id,app.games_dic[x][1].name]);
    }
    eel.edit_games_cart(new_list)();
}

async function del_car_video(id){
    check_del = 1;
    var dic = [];
    let i = 1;
    for(x in app.series_dic){
        if(app.series_dic[x][1].id != id){
            dic.push([i-1,app.series_dic[x][1]]);
            i++;
        }
    }
    app.series_dic = dic;
    var new_list = [];
    for(x in app.series_dic){
        new_list.push([app.series_dic[x][1].id,app.series_dic[x][1].title]);
    }
    if(type == 0){
        eel.edit_series_cart(new_list)();
    }else{
        eel.edit_movies_cart(new_list)();
    }
}


