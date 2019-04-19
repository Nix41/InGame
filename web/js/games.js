async function get_games(){
    let value = await eel.filter_games()();
    let i = 1;
    let list = [];
    app.games_dic = [];
    for (x in value) {
        app.games_dic.push([i-1, value[x]]);
        i++;
    }
    let gens = await eel.get_game_genders()();
    let k = 0;
    for (x in gens){
        Vue.set(app.filter_gen, k, x);
        Vue.set(app.on_mouse, x, 0);
        k++;
    }
    app.categories = gens;
    app.games.push(list);
}
async function filter_games_by_name(){
    app.games = []
    let filter = document.getElementById("name_filter");
    let value = await eel.filter_games(name = app.title, gender = app.filter_selected_subgen, launch=app.year, players=0,game_mode=app.filter_mode, category=app.filter_selected_gen, lenguage=app.filter_language, score=app.filter_score )();
    let i = 1;
    app.games_dic = [];
    for (x in value) {
        app.games_dic.push([i-1, value[x]]);
        i++;
    }
}

function see(id){
    app.name = app.games_dic[id][1].name;
    app.description = app.games_dic[id][1].description;
    app.requirements = app.games_dic[id][1].requirements;
    app.genders = app.games_dic[id][1].genders;
    app.key = id;
    app.launch = app.games_dic[id][1].launch;
    app.score = app.games_dic[id][1].score;
    app.size = app.games_dic[id][1].size;
    app.language = app.games_dic[id][1].language;
    app.gamemode = app.games_dic[id][1].game_mode;
    app.category = app.games_dic[id][1].category;
    app.cover_path = app.games_dic[id][1].cover_path;
    app.captures = app.games_dic[id][1].captures;
    app.current_detail = app.games_dic[id][1].id;
}

function filter_over(gen){
    app.filter_selected_gen = gen.id;
    let g = 0;
    app.filter_subgen = [];
    app.filter_selected_subgen = '';
    for (x in app.categories[gen.id]){
        let l = [];
        l.push(g);
        l.push(app.categories[gen.id][x] );
        app.filter_subgen.push(l);
        g = g + 1;
    }
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
    filter_games_by_name();
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
    app.filter_selected_subgen = app.filter_subgen[sgen][1];
    
    app.filter_subgen_key = app.filter_subgen[sgen][1];
    $("#as" + sgen).css("background-color","rgb(209,4,4)");
    app.filter_subgen_key = app.filter_subgen[sgen][1];
    let i = 0;
    for (x in app.filter_subgen){
        if (sgen != i){
            $("#as" + i).css("background-color","rgb(51,51,51)");
            $("#as" + i).css("margin-top","15px");
            $("#as" + i).css("border-radius","15px");
            $("#as" + i).css("margin-left","10px");
        }
        i++;
    }
    filter_games_by_name();
}

function filter_subgen_mouse(id,x){
        if(x == 1){
            $('#'+ id).css('background-color','rgb(209,4,4)')
        }else{
            $('#'+ id).css('background-color','rgb(51,51,51)')
        }
}

function edit_cleardata(key){
    set_game(app.games_dic[key][1].id);
    app.Max_req=[];
    app.edit_Max_req=[];
    if( app.games_dic[key][1].requirements[1][0].req == "Desconocidos" ){
        app.edit_Max_req.push({'type':'Sistema Operativo:', 'req':app.sO });
        app.edit_Max_req.push({'type':'Memoria:', 'req':app.Memori });
        app.edit_Max_req.push({'type':'Procesador:', 'req':app.Micro });
        app.edit_Max_req.push({'type':'Graficos:', 'req':app.Video });
        app.edit_Max_req.push({'type':'Direct X:', 'req':app.dX });
        app.edit_Max_req.push({'type':'Almacenamiento:', 'req':app.gB });
        app.edit_Max_req.push({'type':'Sonido:', 'req':app.Sound });
        app.edit_Max_req.push({'type':'Notas:', 'req':app.Notes });
    }else{
        for(x in app.games_dic[key][1].requirements[1]){
            app.Max_req.push(app.games_dic[key][1].requirements[1][x]);
            app.edit_Max_req.push(app.games_dic[key][1].requirements[1][x])
        }
    }
    app.Memori='';
    app.Micro='';
    app.Min_req=[];
    app.edit_Min_req=[];
    if(app.games_dic[key][1].requirements[0][0].req == "Desconocidos"){
        app.edit_Min_req.push({'type':'Sistema Operativo:', 'req':app.sO });
        app.edit_Min_req.push({'type':'Memoria:', 'req':app.Memori });
        app.edit_Min_req.push({'type':'Procesador:', 'req':app.Micro });
        app.edit_Min_req.push({'type':'Graficos:', 'req':app.Video });
        app.edit_Min_req.push({'type':'Direct X:', 'req':app.dX });
        app.edit_Min_req.push({'type':'Almacenamiento:', 'req':app.gB });
        app.edit_Min_req.push({'type':'Sonido:', 'req':app.Sound });
        app.edit_Min_req.push({'type':'Notas:', 'req':app.Notes });
    }else{
        for(x in app.games_dic[key][1].requirements[0]){
            app.Min_req.push(app.games_dic[key][1].requirements[0][x]);
            app.edit_Min_req.push(app.games_dic[key][1].requirements[0][x])
        }
    }
    app.Notes='';
    app.Sound='';
    app.Video='';
    app.data='';
    app.file='';
    app.create_prin='';
    app.pgen_check='3';
    app.create_prin = app.games_dic[key][1].category;
    app.create_selected=[];
    for(x in app.games_dic[key][1].genders){
        app.create_selected.push([app.create_selected.length,app.games_dic[key][1].genders[x]]);
    }
    app.req_type='';
    app.create_name=app.games_dic[key][1].name;
    app.create_mode=app.games_dic[key][1].game_mode;
    app.create_year=app.games_dic[key][1].launch;
    app.create_score=app.games_dic[key][1].score;
    app.create_language=app.games_dic[key][1].language;
    app.create_size=app.games_dic[key][1].size;
    app.datas=app.games_dic[key][1].captures;
    app.create_description=app.games_dic[key][1].description;
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

    app.games_dic[app.key][1].name = app.name;
    app.games_dic[app.key][1].description = app.description;
    app.games_dic[app.key][1].requirements = app.requirements;
    app.games_dic[app.key][1].genders = app.genders;
    app.games_dic[app.key][1].launch = app.launch;
    app.games_dic[app.key][1].score = app.score;
    app.games_dic[app.key][1].size = app.size;
    app.games_dic[app.key][1].language = app.language;
    app.games_dic[app.key][1].game_mode = app.create_mode;
    app.games_dic[app.key][1].category = app.category;
    app.games_dic[app.key][1].cover_path = app.cover_path;
    app.games_dic[app.key][1].captures = app.captures;

    update_game(app.name, app.description, app.create_mode, app.language, app.launch, app.score, app.category, app.requirements, app.data, app.datas), size;
}

async function update_game(name, des, mode, language, launch, score, category, requirements, cover, captures, size){
    eel.CRUD_Game(name = name, description = des, game_mode = mode, language = language, launch = launch, puntuacion = score, category = category,genders=[], requirements = requirements,id=-1,cover = cover, captures = captures, size=size)();
}

function del_game(x){
    delete_game(app.games_dic[x][1].id)
    document.location.reload(true);
}

async function delete_game(id){
    eel.CRUD_Game(name="", description="", game_mode="", language="", launch=0, puntuacion=0, category="", genders=[], requirements=[], id=id, cover="", captures=[], 0,1)();
}

//list

function List(){
    app.description='';
    app.name='';
    app.score='';
    app.Max_req='';
    app.Min_req='';
    app.data='';
    app.datas='';
    app.year='';
    app.genders='';
    app.size='';
    app.sinopsis='';
    if(app.list == 0){
        app.list = '1';
    }else{
        app.list = '0';
    }
}

function restore(x){
    let key = x;
    $("#L" + key).css("background-color","rgb(26,26,26)");
    $("#details").css("background-color","rgb(26,26,26)");
}

function change(x){
    let key = x;
    $("#L" + key).css("background-color","rgb(51,51,51)");
    $("#details").css("background-color","rgb(51,51,51)");
    app.description = app.games_dic[x][1].description;
    app.Max_req = app.games_dic[x][1].requirements[1];
    app.Min_req = app.games_dic[x][1].requirements[0];
    app.datas = [];
    for(y=0;y < app.games_dic[x][1].captures.length; y++){
        var list = [];
        list.push(app.games_dic[x][1].captures[y]);
        if(y+1 <= app.games_dic[x][1].captures.length - 1){
            list.push(app.games_dic[x][1].captures[y+1]);
            y++;
        }
        app.datas.push(list)
    }
}