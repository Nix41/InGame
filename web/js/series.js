
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
    //app.description = app.series_dic[id].sinopsis;
    app.genders = app.series_dic[id].genders;
    app.key = id;
    app.launch = app.series_dic[id].year;
    app.score = app.series_dic[id].score;
    app.country = app.series_dic[id].country;
    //app.actors = app.series_dic[id].actors;
    //app.directors = app.series_dic[id].directors;
    app.cover_path = app.series_dic[id].cover_path;
}
