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

function subpush(id){
    app.create_selected.push([app.create_selected.length,app.create_gensub[id][1]]);
    app.pgen_check = 3;
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

function delgen(id){
    delete app.create_selected[id];
    $('#'+id).remove();
}

function delgen_prin(){
    app.pgen_check = 0;
    app.create_prin = '';
}