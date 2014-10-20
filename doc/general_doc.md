#Documentación general

La idea es que despues toda esta doc va a pasar a una wiki

##Debug en OpenShift
Para poder debagear en OpenShift, agrego en home/app-root/repo/wsgi/application:  

    import logging  
    logging.basicConfig(stream = sys.stderr)  

Y el log de python esta en home/app-root/logs/python.log

##Install
    $python setup.py install