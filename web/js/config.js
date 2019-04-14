function false_input(){
    $("#open_file").click();
}

function false_input2(){
    $("#open_file2").click();
}

function agregate_gen(){
    if(app.pgen_check != 1 && app.pgen_check != 2){
        if(app.pgen_check == '0'){
            app.pgen_check = 1;
        }else{
            app.pgen_check = 2;
        }
    }
}

function agregate_gen_prin(){
    app.pgen_check = 1;
}


function push_prin(gen){
    app.create_prin = gen.id;
    app.pgen_check = 3;
}

function push_prin_create(id){
    app.create_prin = app.create_gen[id][1];
    app.pgen_check = 3;
}


function subpush(id){
    app.create_selected.push([app.create_selected.length,app.create_gensub[id][1]]);
    app.pgen_check = 3;
    add_gender_game(app.create_gensub[id][1]);
}

function subpush_create(id){
    app.create_selected.push([app.create_selected.length,app.create_gensub[id][1]]);
    app.pgen_check = 3;
}

async function add_gender_game(name){
    eel.add_game_gender(name)();
}

async function set_game(id){
    eel.Set_Game(id)();
}
function req_type(x){
    app.req_type = x;
    if(x == 0){
        app.Min_req = [];
    }else{
        app.Max_req = [];
    }
}

function req(){
    if(app.req_type == 0){
        app.Min_req.push(['Sistema Operativo:', app.sO ]);
        app.Min_req.push(['Memoria:', app.Memori ]);
        app.Min_req.push(['Procesador:', app.Micro ]);
        app.Min_req.push(['Graficos:', app.Video ]);
        app.Min_req.push(['Direct X:', app.dX ]);
        app.Min_req.push(['Almacenamiento:', app.gB ]);
        app.Min_req.push(['Sonido:', app.Sound ]);
        app.Min_req.push(['Notas:', app.Notes ]);
    }else{
        app.Max_req.push(['Sistema Operativo:', app.sO ]);
        app.Max_req.push(['Memoria:', app.Memori ]);
        app.Max_req.push(['Procesador:', app.Micro ]);
        app.Max_req.push(['Graficos:', app.Video ]);
        app.Max_req.push(['Direct X:', app.dX ]);
        app.Max_req.push(['Almacenamiento:', app.gB ]);
        app.Max_req.push(['Sonido:', app.Sound ]);
        app.Max_req.push(['Notas:', app.Notes ]);
    }
}

function cleardata(){
    app.Max_req=[];
    app.Memori='';
    app.Micro='';
    app.Min_req=[];
    app.Notes='';
    app.Sound='';
    app.Video='';
    app.data='';
    app.file='';
    app.pgen_check='0';
    app.create_selected=[];
    app.req_type='';
    app.create_name='';
    app.create_mode='';
    app.create_year='';
    app.create_score='';
    app.create_language='';
    app.create_size='';
    app.datas=[];
    app.create_description='';
    app.create_prin='';
}

function cleardata_s(){
    app.create_country = '';
    app.create_directors = [];
    app.create_actors = [];
    app.create_name = '';
    app.create_description = '';
    app.create_gen = [];
    app.create_year = '';
    app.create_score = ''; 
    app.create_gen = [];
    app.data = '';
}

function delgen(id){
    del_game_gen(app.create_selected[id][1]);
    delete app.create_selected[id];
    $('#'+id).remove();
}

async function del_game_gen(name){
    eel.del_game_gender(name);
}

function delgen_prin(){
    app.pgen_check = 0;
    app.create_prin = '';
}

function create_game(){
    app.requirements = [];
    app.requirements.push(app.Min_req);
    app.requirements.push(app.Max_req);
    var genders = [];
    for(x in app.create_selected){
        genders.push(app.create_selected[x][1])
    }
    create_game_for_real(app.create_name, app.create_description, app.create_mode, app.create_language, app.create_year, app.create_score, app.create_prin, app.requirements, app.data, app.datas, genders, app.create_size);
}

async function create_game_for_real(name, des, mode, language, launch, score, category, requirements, cover, captures, genders){
    eel.CRUD_Game(name = name, description = des, game_mode = mode, language = language, launch = launch, puntuacion = score, category = category,genders=genders, requirements = requirements,id=-1,cover = cover, captures = captures)();
}

function create_video(type){
    app.name = app.create_name;
    app.description = app.create_description;
    app.launch = app.create_year;
    app.country = app.create_country;
    app.score = app.create_score;
    var gen = [];
    for(x in app.create_gen){
        if(app.create_gen[x][0] >= 0){
            gen.push(app.create_gen[x][1]);
        }
    }
    var dir = [];
    for(x in app.create_directors){
        if(app.create_directors[x][0] >= 0){
            dir.push(app.create_directors[x][1]);
        }
    }
    var act = [];
    for(x in app.create_actors){
        if(app.create_actors[x][0] >= 0){
            act.push(app.create_actors[x][1]);
        }
    }
    if(app.data != ''){
        app.cover_path = app.data;
    }


    create_video_back(app.name, app.description, app.launch, app.country, app.score, type, gen, dir, act);
}

async function create_video_back(name, description, year, country, score, type, gen, dir, act){
    if(type == 's'){
        await eel.CRUD_Serie(title=name, year=year, pais=country,sinopsis=description, genero=gen,directors=dir,reparto=act,score=score, id=-1,image=app.data)();
        window.location.reload(true);
    }else{
        await eel.CRUD_Movie(title=name, year=year, pais=country,sinopsis=description, genero=gen,directors=dir,reparto=act,score=score, id=-1,image=app.data)();
        window.location.reload(true);
    }
    
}

async function download_games(){
    r = await eel.download_games()();
    if (r == -1){
        alert('No tienes conexion a internet, compruebe su conexion e intentelo mas tarde')
    }
    if (r == 2){
        alert('Comenzando Descarga en la consola')
    }
}

async function download_series(){
    r = await eel.download_series()();
    if (r == -1){
        alert('No tienes conexion a internet, compruebe su conexion e intentelo mas tarde')
    }
     if (r == 2){
        alert('Comenzando Descarga en la consola')
    }
}

async function download_movies(){
    r = await eel.download_movies()();
    if (r == -1){
        alert('No tienes conexion a internet, compruebe su conexion e intentelo mas tarde')
    }
     if (r == 2){
        alert('Comenzando Descarga en la consola')
    }
}

async function gen_pdf(){
    
}