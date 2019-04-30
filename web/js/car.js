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