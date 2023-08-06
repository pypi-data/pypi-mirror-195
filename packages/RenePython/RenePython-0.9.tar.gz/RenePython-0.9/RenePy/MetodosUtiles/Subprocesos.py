# import schedule
# import time
# import sched
import threading
from pytz import utc
from multiprocessing import Process
# from apscheduler.schedulers.blocking import BlockingScheduler
#
# scheduler = BlockingScheduler(timezone=utc)
from apscheduler.schedulers.background import BackgroundScheduler
from RenePy.ClasesUtiles.Date import Date

class Job_Automatico:
    def __init__(self,scheduler,job):
        self.__scheduler=scheduler
        self.__job=job
    def pause(self):
        self.__job.pause()
    def resume(self):
        self.__job.resume()
    def detener(self):
        self.__scheduler.shutdown()
    def modificar(self,dias='*',horas='*',minutos='*',segundos='*',timeZoneCuba=True):
        metodo=self.__job.func
        self.__job.remove()
        if timeZoneCuba and horas != '*':
            horas = str((int(horas) + 5) % 24)
        ld = [dias, horas, minutos, segundos]
        ponerA0 = False
        for i in range(len(ld)):
            if ld[i] != '*':
                ponerA0 = True
                continue
            if ponerA0:
                ld[i] = 0
        self.__job=self.__scheduler.add_job(metodo, 'cron', day_of_week=ld[0], hour=ld[1], minute=ld[2], second=ld[3])
        return self
    def proximaEjecucion(self):
        return Date(self.__job.next_run_time)


def executeTodosLos(metodo,dias='*',horas='*',minutos='*',segundos='*',timeZoneCuba=True):
    scheduler = BackgroundScheduler(timezone=utc)
    if timeZoneCuba and horas!='*':
        horas=str((int(horas)+5)%24)
    ld=[dias,horas,minutos,segundos]
    ponerA0=False
    for i in range(len(ld)):
        if ld[i]!='*':
            ponerA0=True
            continue
        if ponerA0:
            ld[i]=0
    this_job=scheduler.add_job(metodo, 'cron', day_of_week=ld[0], hour=ld[1], minute=ld[2], second=ld[3])
    scheduler.start()
    return Job_Automatico(scheduler,this_job)



def subproceso(accion):
    p = Process(target=accion, args=())#'bob',
    p.start()
    return p
def detenerSubproceso(subproceso):
    if isinstance(subproceso,Process):
        subproceso.terminate()
def esperar(segundos):
    c = threading.Condition()
    c.acquire()
    c.wait(segundos)
    return c





# import datetime
# def some_job():
#     print("Decorated job")
#     print(datetime.datetime.now())
#
# executeTodosLos(some_job,segundos=0)

#scheduler.add_job(some_job, 'interval', seconds=1)


# while True:
#     pass

# def job():
#     print("I'm working...")
#     # ejecutar()
#
# def ejecutar():
#     schedule.every().seconds.do(job)
#     schedule.run_pending()
#
# hilo = threading.Thread(target=ejecutar)
# hilo.start()
# # print("Comienza")
# while True:
#     pass

# s = sched.scheduler(time.time, time.sleep)
# def print_time(a='default'):
#     print("From print_time", time.time(), a)
# def print_some_times():
#     print(time.time())
#     s.enter(10, 1, print_time)
#     s.enter(5, 2, print_time, argument=('positional',))
#     s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
#     s.run()
#     print(time.time())
#
# print_some_times()