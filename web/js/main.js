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