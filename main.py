from controllers.main_controller import MainController
# Programme principal
if __name__ == '__main__':
    
    try:
        main_controller = MainController()
        main_controller.run()
    except KeyboardInterrupt:
        print("Arret du programme")