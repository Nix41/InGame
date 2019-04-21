from WebScrapping import Down_Games, Down_Movies, Down_Series

def downgames():
    current_process = Process(target= Down_Games)
    current_process.start()
    return current_process

def downseries():
    current_process = Process(target= Down_Series)
    current_process.start()
    return current_process

def downmovies():
    current_process = Process(target= Down_Movies)
    current_process.start()
    return current_process
