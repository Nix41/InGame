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
    let value = await eel.filter_games(name = app.title, gender = app.filter_subgen_selected, launch=app.year, players=0,game_mode=app.filter_mode, category=app.filter_selected_gen, lenguage=app.filter_language, score=app.filter_score )();
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
    app.cover_path = app.games_dic[id].cover_path;
    app.captures = app.games_dic[id].captures;
}

function filter_over(gen){
    app.filter_selected_gen = gen.id;
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

function filter_subgen_clk(sgen){
    app.filter_subgen_selected = app.filter_subgen[sgen][1];
    alert(app.filter_subgen[sgen][1]);
}

function filter_subgen_mouse(id,x){
        if(x == 1){
            $('#'+ id).css('background-color','rgb(209,4,4)')
        }else{
            $('#'+ id).css('background-color','rgb(51,51,51)')
        }
}

function edit_cleardata(key){
    set_game(app.games_dic[key].id);
    app.Max_req=[];
    app.edit_Max_req=[];
    if( app.games_dic[key].requirements[1][0].req == "Desconocidos" ){
        app.edit_Max_req.push({'type':'Sistema Operativo:', 'req':app.sO });
        app.edit_Max_req.push({'type':'Memoria:', 'req':app.Memori });
        app.edit_Max_req.push({'type':'Procesador:', 'req':app.Micro });
        app.edit_Max_req.push({'type':'Graficos:', 'req':app.Video });
        app.edit_Max_req.push({'type':'Direct X:', 'req':app.dX });
        app.edit_Max_req.push({'type':'Almacenamiento:', 'req':app.gB });
        app.edit_Max_req.push({'type':'Sonido:', 'req':app.Sound });
        app.edit_Max_req.push({'type':'Notas:', 'req':app.Notes });
    }else{
        for(x in app.games_dic[key].requirements[1]){
            app.Max_req.push(app.games_dic[key].requirements[1][x]);
            app.edit_Max_req.push(app.games_dic[key].requirements[1][x])
        }
    }
    app.Memori='';
    app.Micro='';
    app.Min_req=[];
    app.edit_Min_req=[];
    if(app.games_dic[key].requirements[0][0].req == "Desconocidos"){
        app.edit_Min_req.push({'type':'Sistema Operativo:', 'req':app.sO });
        app.edit_Min_req.push({'type':'Memoria:', 'req':app.Memori });
        app.edit_Min_req.push({'type':'Procesador:', 'req':app.Micro });
        app.edit_Min_req.push({'type':'Graficos:', 'req':app.Video });
        app.edit_Min_req.push({'type':'Direct X:', 'req':app.dX });
        app.edit_Min_req.push({'type':'Almacenamiento:', 'req':app.gB });
        app.edit_Min_req.push({'type':'Sonido:', 'req':app.Sound });
        app.edit_Min_req.push({'type':'Notas:', 'req':app.Notes });
    }else{
        for(x in app.games_dic[key].requirements[0]){
            app.Min_req.push(app.games_dic[key].requirements[0][x]);
            app.edit_Min_req.push(app.games_dic[key].requirements[0][x])
        }
    }
    app.Notes='';
    app.Sound='';
    app.Video='';
    app.data='';
    app.file='';
    app.create_prin='';
    app.pgen_check='3';
    app.create_prin = app.games_dic[key].category;
    app.create_selected=[];
    for(x in app.games_dic[key].genders){
        app.create_selected.push([app.create_selected.length,app.games_dic[key].genders[x]]);
    }
    app.req_type='';
    app.create_name=app.games_dic[key].name;
    app.create_mode=app.games_dic[key].game_mode;
    app.create_year=app.games_dic[key].launch;
    app.create_score=app.games_dic[key].score;
    app.create_language=app.games_dic[key].language;
    app.create_size=app.games_dic[key].size;
    app.datas=app.games_dic[key].captures;
    app.create_description=app.games_dic[key].description;
}

function add_req(n){
    if(n == 1){
        app.Max_req = [];
        for(x in app.edit_Max_req){
            app.Max_req.push(app.edit_Max_req[x]);
            if(app.edit_Max_req[x].req = ""){
                app.Max_req[app.Max_req.length - 1].req = 'Desconocidos';
            }
        }
    }else{
        app.Min_req = [];
        for(x in app.edit_Min_req){
            app.Min_req.push(app.edit_Min_req[x]);
            if(app.edit_Min_req[x].req = ""){
                app.Min_req[app.Max_req.length - 1].req = 'Desconocidos';
            }
        }
    }
}

function editcheck(x){
    app.edit_check = x;
}

function add_game(){
    app.name= app.create_name;
    app.requirements[0]= app.Min_req;
    app.requirements[1]= app.Max_req;
    app.score=app.create_score;
    app.size=app.create_size;
    app.language=app.create_language;
    app.gamemode=app.create_mode;
    app.category=app.create_prin;
    app.genders = [];
    for(x in app.create_selected){
        if(app.create_selected[x] != undefined){
            app.genders.push(app.create_selected[x][1]);
        }
    }
    app.description= app.create_description;
    app.launch= app.create_year;
    if(app.data != ''){
        app.cover_path = app.data;
    }
    app.captures = app.datas;

    app.games_dic[app.key].name = app.name;
    app.games_dic[app.key].description = app.description;
    app.games_dic[app.key].requirements = app.requirements;
    app.games_dic[app.key].genders = app.genders;
    app.games_dic[app.key].launch = app.launch;
    app.games_dic[app.key].score = app.score;
    app.games_dic[app.key].size = app.size;
    app.games_dic[app.key].language = app.language;
    app.games_dic[app.key].game_mode = app.create_mode;
    app.games_dic[app.key].category = app.category;
    app.games_dic[app.key].cover_path = app.cover_path;
    app.games_dic[app.key].captures = app.captures;

    fil = (app.key - app.key%5)/5;
    id = app.key%5 - 1

    app.games[fil][id].name = app.name;
    app.games[fil][id].description = app.description;
    app.games[fil][id].requirements = app.requirements;
    app.games[fil][id].genders = app.genders;
    app.games[fil][id].launch = app.launch;
    app.games[fil][id].score = app.score;
    app.games[fil][id].size = app.size;
    app.games[fil][id].language = app.language;
    app.games[fil][id].game_mode = app.create_mode;
    app.games[fil][id].category = app.category;
    app.games[fil][id].cover_path = app.cover_path;
    app.games[fil][id].captures = app.captures;

    update_game(app.name, app.description, app.create_mode, app.language, app.launch, app.score, app.category, app.requirements, app.data, app.datas);
}

async function update_game(name, des, mode, language, launch, score, category, requirements, cover, captures){
    eel.CRUD_Game(name = name, description = des, game_mode = mode, language = language, launch = launch, puntuacion = score, category = category,genders=[], requirements = requirements,id=-1,cover = cover, captures = captures)();
}

function del_game(x){
    alert(app.games_dic[x].id)
   delete_game(app.games_dic[x].id)
}

async function delete_game(id){
    eel.CRUD_Game(name="", description="", game_mode="", language="", launch=0, puntuacion=0, category="", genders=[], requirements=[], id=id, cover="", captures=[], 1)();
}

