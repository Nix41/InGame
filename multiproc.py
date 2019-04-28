from WebScrapping import Down_Games, Down_Movies, Down_Series
import multiprocessing as mp


if __name__ == 'multiproc': 
    print('here')
    def downgames():
        current_process = mp.Process(target= Down_Games)
        current_process.start()
        return current_process

    def downseries():
        current_process = mp.Process(target= Down_Series)
        current_process.start()
        return current_process

    def downmovies():
        current_process = mp.Process(target= Down_Movies)
        current_process.start()
        return current_process

