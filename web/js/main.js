Vue.component('banner',{
    data: function(){
        return{
            url : '',
        }
    },
    template: `
    <nav class='justify-content-center'>
        <img src='img/banner_new.png' class='card-img rounded-0 img-fluid ingame-navbar' alt='Responsive image'>
        <div style="width:430px; margin-top:-150px; margin-left:10px;">
            <img src='img/ingame-05.png' style="height: 8vw; width:100%; margin:0 important; object-fit: cover;" class='card-img rounded-0 img-fluid ingame-navbar' alt='Responsive image'>
        </div>
        <ul class='card-img-overlay d-block navbar-nav d-flex flex-row-reverse'>
            <li class='p-2 nav-item'>
                <a href='config_vue.html'>
                    <div v-if="url == '4'">
                        <img src='img/admin_active.png' class='img-fluid nav-menu-item' alt='Responsive image'>
                    </div>
                    <div v-else>
                        <img src='img/config_item.png' class='img-fluid nav-menu-item' alt='Responsive image'>
                    </div>
                </a>
            </li>
            <li class='p-2 nav-item'>
                <a href='films_vue.html'>
                <div v-if="url == '3'">
                    <img src='img/films_active.png' class='img-fluid nav-menu-item' alt='Responsive image'>
                </div>
                <div v-else>
                    <img src='img/films_item.png' class='img-fluid nav-menu-item' alt='Responsive image'>
                </div>
                </a>
            </li>
            <li class='p-2 nav-item'>
                <a href='series_vue.html'>
                <div v-if="url == '2'">
                    <img src='img/series_active.png' class='img-fluid nav-menu-item' alt='Responsive image'>
                </div>
                <div v-else>
                    <img src='img/series_item.png' class='img-fluid nav-menu-item' alt='Responsive image'>
                </div>
                </a>
            </li>
            <li class='p-2 nav-item'>
                <a href='games_vue.html'>
                    <div v-if='url == "game"'>
                        <img src='img/games_active.png' class='img-fluid nav-menu-item' alt='Responsive image'>
                    </div>
                    <div v-else>
                        <img src='img/games_item.png' class='img-fluid nav-menu-item' alt='Responsive image'>
                    </div>
                </a>
            </li>
            <li class='p-2 nav-item'>
                <a href='index_vue.html'>
                    <div v-if="url == '0'">
                        <img src='img/home_active.png' class='img-fluid nav-menu-item' alt='Responsive image'>
                    </div>
                    <div v-else>
                        <img src='img/home_item.png' class='img-fluid nav-menu-item' alt='Responsive image'>
                    </div>
                </a>
            </li>
        </ul>
    </nav>
    `,
});

Vue.component('footerv', {
    template:`
    <!-- Footer top section -->
    <section class="footer-top-section" style="height: 400px;">
        <div class="footer-logo text-white" style="text-align: center; margin-top:-50px;">
            <img src="img/logo_banner.png" style="width:350px;" class="img-fluid" alt="">
            <p>Yasmany IN-GAME PC-SERIES-FIMLS</p>
            <p class="copyright"><!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
            Copyright &copy;<script>document.write(new Date().getFullYear());</script> All rights reserved | This application is made by <a href="#" target="_blank">Aylin && Andres</a>
            <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
            </p>
        </div>
        <div class="footer-top-bg">
            <img src="img/footer-top-bg.png" class="img-fluid" alt="">
        </div>
    </section>
    <!-- Footer top section end -->
    `,
});

var app = new Vue({
    el: '#root',
    data: {
        recent: [],
        games: [],
        games_dic: [],
        Temp: [0,1,2,3,4,5,6,7,8],
        url:'',
        current_detail:'',

        //list Mode
        list:'0',
        list_select:'0',

        counters:[],
        //series
        series_dic:[],
        series : [],
        country:'',
        actors:[],
        directors:[],
        sinopsis:'',
        create_actors:[],
        create_directors:[],
        create_country:'',
        create_video_gen:'',
        create_dic:'',
        create_act:'',
        dic_check:'0',
        act_check:'0',

        //game_select
            //games_dic_key
            games_low_key: 1,
            games_higth_key: 1,
        name: '',
        key: '',
        requirements: [[],[]],
        score:'',
        size:'',
        language:'',
        gamemode:'',
        category:'',
        description: '',
        genders: [],
        launch: '',
        cover_path: '',
        captures: '',

        //filter_vew
        filter_gen:{},
        filter_video_gen:[],
        filter_subgen:[[0,"Acción táctica"],[1,"Acción y aventura,Battle royale"],[2,"Beat'em up,Hack and Slash"],[3,"Lucha"],[4,"Plataformas"],[5,"Primera persona (FPS)"],[6,"Runner"],[7,"Shoot'Em Up"],[8,"Shooter"],[9,"Supervivencia"],[10,"Survival horror"]],
        on_mouse: {},
        categories:{},
        filter_key: '',
        filter_subgen_key:'',
        filter_selected_gen:'',
        filter_selected_gens:[],
        filter_selected_subgen:'',
        filter_topic:'',
        
        //filters
        number:'',
        year:'',
        title:'',
        filter_language:'',
        filter_score:'',
        filter_mode:'',
        //edit
        edit_Min_req:[],
        edit_Max_req:[],
        edit_check:'',
        //agregate
        file:'',
        data:'',
        datas:[],
        create_gen:{1:[1,'Acción'], 2:[2,'Aventuras'], 3:[3,'Casual'], 4:[4,'Conducción'], 5:[5,'Deportes'], 6:[6,'Estrategia'], 7:[7,'MMO'], 8:[8,'Rol'], 9:[9,'Simulación']},
        create_gensub:[[0,"Acción táctica"],[1,"Acción y aventura,Battle royale"],[2,"Beat'em up,Hack and Slash"],[3,"Lucha"],[4,"Plataformas"],[5,"Primera persona (FPS)"],[6,"Runner"],[7,"Shoot'Em Up"],[8,"Shooter"],[9,"Supervivencia"],[10,"Survival horror"]],
        pgen_check:'0',
        create_selected:[],
        sO:'',
        Micro:'',
        Memori:'',
        Video:'',
        dX:'',
        gB:'',
        Sound:'',
        Notes:'',
        Min_req: [],
        Max_req: [],
        req_type: '',
        create_name:'',
        create_mode:'',
        create_year:'',
        create_score:'',
        create_language:'',
        create_size:'',
        create_description:'',
        create_prin:'',
    },

    methods:{
        prevent: function(e)
        {
           if(e) e.preventDefault();
           console.log("Filter in progress ...");
        },

        check_num(){
            if(this.number != '' && this.number > 50 || this.number < 0){
                alert("El numero debe ser mayor que 1 y menor que 51");
                this.number = '';
            }
        },

        check_year(){
            if(this.year != '' && this.year > 3000 || this.year < 0){
                alert("El numero debe ser mayor que 1980 y menor que 3000");
                this.year = '';
            }
        },

        check_score(){
            if(this.filter_score != '' && (this.filter_score > 10 || this.filter_score < 0)){
                alert("El numero debe ser mayor que 1 y menor que 10");
                this.score = '';
            }
        },

        cat_image: function(event){
            var input = event.target;
            if(input.files && input.files[0]){
                var reader = new FileReader();
                reader.onload = (e) => {
                    this.data = e.target.result;
                }
                reader.readAsDataURL(input.files[0]);
            }

        },

        cat_images: function(event){
            var input = event.target;
            for(i = 0; i < input.files.length; i++){
                if(input.files && input.files[i]){
                    var reader = new FileReader();
                    reader.onload = (e) => {
                        this.datas.push(e.target.result);
                    }
                    reader.readAsDataURL(input.files[i]);
                }
            }

        },
    },

    var: 0,
});

async function get_recent(){
    let value = await eel.get_recent()();
    i = 0;
    for (x in value) {
        app.recent.push(value[x]);
    }
}


async function OnNext(i=1,t='g'){
    var element = await eel.get_more(i)();
    app.games_dic = [];
    app.series_dic = [];
    for (x in element){
        if(t == 'g'){
            app.games_dic.push([x,element[x]]);
        }else{
            app.series_dic.push([x,element[x]]);
        }
    }
}

async function SingleNext(dir = 1, typ='g'){
    var id = app.current_detail;
    var element = await eel.next_obj(id, dir)();
    if (typ == 'g'){
        app.name = element.name;
        app.description = element.description;
        app.requirements = element.requirements;
        app.genders = element.genders;
        app.category = element.category;
        app.score = element.score;
        app.size = element.size;
        app.launch = element.launch;
        app.language = element.language;
        app.gamemode = element.game_mode;
        app.cover_path = element.cover_path;
        app.captures = element.captures;
        app.current_detail = element.id;
    }
    else{
        app.name = element.title;
        app.description = element.sinopsis;
        app.genders = element.genders;
        app.launch = element.year;
        app.score = element.score;
        app.country = element.country;
        app.actors = [];
        app.current_detail = element.id;
        for(x in element.actors){
            app.actors.push([x,element.actors[x]]);
        }
        app.directors = [];
        for(x in element.directors){
            app.directors.push([x,element.directors[x]]);
        }
        app.cover_path = element.cover_path
    }
   
}
