
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

async function filter_series_all(typ ='s'){
    app.series = []
    let value = [];
    if (typ == 's'){
        value = await eel.filter_series(name=app.title , gender="", actor=app.filter_language, director=app.filter_mode, score=app.filter_score, year=app.year )();
    }
    else{
        value = await eel.filter_movies(name=app.title , gender="", actor=app.filter_language, director=app.filter_mode, score=app.filter_score, year=app.year )();
    }
    let i = 1;
    let list = [];
    app.series_dic = {}
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

function series_edit_cleardata(id, type = 's'){
        app.key = id;
        set_video(id,type);
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
            app.create_gen.push([x,app.genders[x]]);
        }
        app.create_year = app.launch;
        app.create_score = app.score; 
}

async function set_video(id,type){
    if(type == 's'){
        eel.Set_Serie(id)();
    }else{
        eel.Set_Movie(id)();
    }
}

function agregate_gen_video(type = 's'){
    app.create_gen.push([app.create_gen.length,app.create_video_gen]);
    app.pgen_check = 0;
    add_tv_gender(app.create_video_gen, type);
}

async function add_tv_gender(gen, type = 's'){
    if(type == 's'){
        alert('aqui');
        eel.add_tv_gender(gen, false)();
    }else{
        alert('where i should be');
        eel.add_tv_gender(gen, true)();
    }
}

function delgenvideo(id){
    del_tv_gender(app.create_gen[id][1]);
    app.create_gen[id][0] = -1*id;
    $('#'+id).remove();
}

async function del_tv_gender(gen){
    eel.del_tv_gender(gen)();
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
    add_director(app.create_dic);
}

async function add_director(dir){
    eel.add_director(dir)();
}

function deldic(id){
    del_director(app.create_directors[id][1]);
    app.create_directors[id][0] = -1*id;
    $('#D'+id).remove();
}

async function del_director(dir){
    eel.del_director(dir)();
}

function delact(id){
    del_actor(app.create_actors[id][1]);
    app.create_actors[id][0] = -1*id;
    $('#A'+id).remove();
}

async function del_actor(dir){
    eel.del_actor(dir)();
}

function addact(){
    app.act_check = 1;
}

function pushact(){
    app.create_actors.push([app.create_actors.length,app.create_act]);
    app.act_check = 0;
    add_actor(app.create_act)
}

async function add_actor(dir){
    eel.add_actor(dir)();
}

function add_video(type){
    app.name = app.create_name;
    app.description = app.create_description;
    app.launch = app.create_year;
    app.country = app.create_country;
    app.score = app.create_score;
    if(app.data != ''){
        app.cover_path = app.data;
    }


    add_video_back(app.name, app.description, app.launch, app.country, app.score, type);
}
async function add_video_back(name, description, year, country, score, type){
    if(type == 's'){
        await eel.CRUD_Serie(title=name, year=year, pais=country,sinopsis=description, genero=[],directors=[],reparto=[],score=score, id=-1,image=app.data)();
        window.location.reload(true);
    }else{
        await eel.CRUD_Movie(title=name, year=year, pais=country,sinopsis=description, genero=[],directors=[],reparto=[],score=score, id=-1,image=app.data)();
        window.location.reload(true);
    }
    
}
//list

function List_s(){
    app.sinopsis='';
    app.name='';
    app.score='';
    app.year='';
    app.genders='';
    if(app.list == 0){
        app.list = '1';
    }else{
        app.list = '0';
    }
}

function restore_s(x){
    let key = x;
    $("#L" + key).css("background-color","rgb(26,26,26)");
    $("#details").css("background-color","rgb(26,26,26)");
}

function change_s(x){
    let key = x;
    $("#L" + key).css("background-color","rgb(51,51,51)");
    $("#details").css("background-color","rgb(51,51,51)");
    app.sinopsis = app.series_dic[x].sinopsis;
    app.cover_path = app.series_dic[x].cover_path;
    app.directors = [];
    for (d in app.series_dic[x].directors){
        app.directors.push(app.series_dic[x].directors[d])
    }
    app.actors = [];
    for (d in app.series_dic[x].actors){
        app.actors.push(app.series_dic[x].actors[d])
    }
}

function list_red(){
    app.list_select = 1;
}

function list_gray(){
    app.list_select = 0;
}

async function del_serie(key){
    await eel.CRUD_Serie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],score=0,id=key, image="", topics=[], 1)();
    document.location.reload(true);
}

async function del_movie(key){
    await eel.CRUD_Movie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],score=0,id=key, image="", topics=[], 1)();
    document.location.reload(true);
}
