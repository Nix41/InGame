
async function get_series(){
    let value = await eel.filter_series()();
    let i = 1;
    let list = [];
    for (x in value) {
        Vue.set(app.series_dic, x, value[x]);
        if(i%5 == 0){
            list.push(value[x]);
            app.series.push(list);
            list = [];
        }else{
            list.push(value[x]);
        }
        key = "id" + i;
        i++;
    }
    app.series.push(list);
}

async function get_films(){
    let value = await eel.filter_movies()();
    let i = 1;
    let list = [];
    for (x in value) {
        Vue.set(app.series_dic, x, value[x]);
        if(i%5 == 0){
            list.push(value[x]);
            app.series.push(list);
            list = [];
        }else{
            list.push(value[x]);
        }
        key = "id" + i;
        i++;
    }
    app.series.push(list);
}

function see_s(id){
    app.name = app.series_dic[id].title;
    app.description = app.series_dic[id].sinopsis;
    app.genders = app.series_dic[id].genders;
    app.key = id;
    app.launch = app.series_dic[id].year;
    app.score = app.series_dic[id].score;
    app.country = app.series_dic[id].country;
    app.actors = [];
    for(x in app.series_dic[id].actors){
        app.actors.push([x,app.series_dic[id].actors[x]]);
    }
    app.directors = [];
    for(x in app.series_dic[id].directors){
        app.directors.push([x,app.series_dic[id].directors[x]]);
    }
    app.cover_path = app.series_dic[id].cover_path;
}

function series_edit_cleardata(id){
        app.create_country = app.country;
        app.create_directors = [];
        for(x in app.directors){
            app.create_directors.push(app.directors[x]);
        }
        app.create_actors = [];
        for(x in app.actors){
            app.create_actors.push(app.actors[x]);
        }
        app.create_name = app.name;
        app.create_description = app.description;
        app.create_gen = [];
        for(x in app.genders){
            app.create_gen.push([x, app.genders[x]]);
        }
        app.create_year = app.launch;
        app.create_score = app.score; 
}

function agregate_gen_video(){
    app.create_gen.push([app.create_gen.length,app.create_video_gen]);
    app.pgen_check = 0;
}

function delgenvideo(id){
    delete app.create_gen[id];
    $('#'+id).remove();
}

function agregate_dic(){
    if(app.dic_check != 1 && app.dic_check != 2){
        if(app.dic_check == '0'){
            app.dic_check = 1;
        }else{
            app.dic_check = 2;
        }
    }
}

function push_dic(){
    app.create_directors.push([app.create_directors.length,app.create_dic]);
    app.dic_check = 0;
}

function deldic(id){
    delete app.create_directors[id];
    $('#D'+id).remove();
}

function delact(id){
    delete app.create_actors[id];
    $('#A'+id).remove();
}

function addact(){
    app.act_check = 1;
}

function pushact(){
    app.create_actors.push([app.create_actors.length,app.create_act]);
    app.act_check = 0;
}