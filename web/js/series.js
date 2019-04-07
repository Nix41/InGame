
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
    app.s_name = app.series_dic[id].title;
    app.s_description = app.games_dic[id].sinopsis;
    app.s_genders = app.games_dic[id].genders;
    app.s_key = id;
    app.s_launch = app.games_dic[id].year;
    app.s_score = app.games_dic[id].score;
    app.s_country = app.games_dic[id].country;
    app.s_actors = app.games_dic[id].actors;
    app.s_directors = app.games_dic[id].directors;
    app.s_cover_path = app.games_dic[id].cover_path;
}
