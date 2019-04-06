Vue.component('banner',{
    template: `
    <nav class='fixed-top justify-content-center'>
        <img src='img/banner_new.jpg' class='card-img rounded-0 img-fluid ingame-navbar' alt='Responsive image'>
        <ul class='card-img-overlay d-block navbar-nav d-flex flex-row-reverse'>
            <li class='p-2 nav-item'>
                <a href='config_vue.html'>
                    <img src='img/config_item.png' class='img-fluid nav-menu-item' alt='Responsive image'>
                </a>
            </li>
            <li class='p-2 nav-item'>
                <a href='films_vue.html'>
                    <img src='img/films_item.png' class='img nav-menu-item' alt='Responsive image'>
                </a>
            </li>
            <li class='p-2 nav-item'>
                <a href='series_vue.html'>
                    <img src='img/series_item.png' class='img-fluid nav-menu-item' alt='Responsive image'>
                </a>
            </li>
            <li class='p-2 nav-item'>
                <a href='games_vue.html'>
                    <img src='img/games_item.png' class='img nav-menu-item' alt='Responsive image'>
                </a>
            </li>
            <li class='p-2 nav-item'>
                <a href='index_vue.html'>
                    <img src='img/home_item.png' class='img-fluid nav-menu-item' alt='Responsive image'>
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
        <div class="footer-logo text-white" style="text-align: center;">
            <img src="img/sitio_ingame_logo.png" class="img-fluid" alt="">
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
        games_dic: {},
        key: '',
        games_dic: {},
        name: '',
        description: '',
        genders: [],
        requirements: '',
        launch: '',
        score:'',
        size:'',
        language:'',
        gamemode:'',
        category:'',
        Temp: [0,1,2,3,4,5,6,7,8],

        //filter_vew
        filter_gen:{0:'Todos', 1:'Acción', 2:'Aventuras', 3:'Casual', 4:'Conducción', 5:'Deportes', 6:'Estrategia', 7:'MMO', 8:'Rol', 9:'Simulación'},
        filter_subgen:[[0,"Acción táctica"],[1,"Acción y aventura,Battle royale"],[2,"Beat'em up,Hack and Slash"],[3,"Lucha"],[4,"Plataformas"],[5,"Primera persona (FPS)"],[6,"Runner"],[7,"Shoot'Em Up"],[8,"Shooter"],[9,"Supervivencia"],[10,"Survival horror"]],
        on_mouse: {'Todos':0, 'Acción':0, 'Aventuras':0, 'Casual':0, 'Conducción':0, 'Deportes':0, 'Estrategia':0, 'MMO':0, 'Rol':0, 'Simulación':0},
        filter_key: '',
        //filters
        number:'',
        year:'',
        title:'',
        language:'',
        score:'',

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
    },

    methods:{
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
            if(this.score != '' && (this.score > 10 || this.score < 0)){
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

function active_item(){
    
}