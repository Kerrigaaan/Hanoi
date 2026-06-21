from engine import Pole, Disk
from engine.scene import IsMoveValid, IsGameOver


def test_is_move_valid(is_move_valid: IsMoveValid):
    poles = {
        'A': Pole(_disks=[]),
        'B': Pole(_disks=[Disk(width=3.)]),
        'C': Pole(_disks=[Disk(width=4.)])
    }
    assert is_move_valid(poles, 'B', 'C'), \
        "Déplacer un disque plus petit que le disque de destination n'a pas été considéré"
    assert is_move_valid(poles, 'B', 'A'), \
        "Déplacer d'un disque vers un emplacement sans disque n'a pas été considéré"
    assert not is_move_valid(poles, 'A', 'B'), \
        "Déplacer depuis un emplacement sans disque n'a pas été considéré"
    assert not is_move_valid(poles, 'C', 'B'), \
        "Déplacer un disque plus grand que le disque de destination n'a pas été considéré"
    # assert not is_move_valid(poles, 'z', 'A'), \
    #     "Utiliser un poteau source inexistant (ici 'z') n'a pas été considéré"
    # assert not is_move_valid(poles, 'B', 'z'), \
    #     "Utiliser un poteau de destination inexistant (ici 'z') n'a pas été considéré"


def test_is_game_over(is_game_over: IsGameOver, strict: bool):
    poles = {
        'A': Pole(_disks=[Disk(width=i + 1) for i in range(3)]),
        'B': Pole(_disks=[]),
        'C': Pole(_disks=[]),
    }
    assert not is_game_over(poles), "Le cas où les disques sont sur le poteau A n'a pas été géré."

    poles = {
        'A': Pole(_disks=[]),
        'B': Pole(_disks=[Disk(width=i + 1) for i in range(3)]),
        'C': Pole(_disks=[]),
    }
    assert is_game_over(poles) != strict, \
        "Le cas où tous les disques sont sur le poteau B n'a pas été géré."

    poles = {
        'A': Pole(_disks=[]),
        'B': Pole(_disks=[]),
        'C': Pole(_disks=[Disk(width=i + 1) for i in range(3)]),
    }
    assert is_game_over(poles), \
        "Le cas où tous les disques sont sur le poteau C n'a pas été géré."
    
    poles = {
        'A': Pole(_disks=[]),
        'B': Pole(_disks=[Disk(width=1)]),
        'C': Pole(_disks=[Disk(width=2)]),
    }
    assert not is_game_over(poles), \
        "Le cas où les disques sont répartis sur B et C n'a pas été géré."


def check_function(func, test_func):
    try:
        test_func(func)
        print('\u2705 Tous les tests sont passés !')
    except AssertionError as e:
        print(f'\u274c {e}')
    except NameError as e:
        import re
        m   = re.search(r"name '([^']+)' is not defined", str(e))
        nom = m.group(1) if m else str(e)
        print(f"\u274c Le nom \u00ab {nom} \u00bb n'est pas reconnu. V\u00e9rifie l'orthographe, "
              f"ou qu'il est bien d\u00e9fini avant d'\u00eatre utilis\u00e9.")
    except Exception as e:
        print(f'\u274c Ton code a levé une exception : {type(e).__name__}, {e}')


def check_is_move_valid(func):
    check_function(func, test_is_move_valid)


def check_is_game_over(func, strict=False):
    check_function(func, lambda *args, **kwargs: test_is_game_over(*args, **kwargs, strict=strict))
