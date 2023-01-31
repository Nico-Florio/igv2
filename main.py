from selenium import webdriver
import time
import getpass
import os



def obtener_usuario():
    usuario_ok: bool = False
    while not usuario_ok:
        try:
            usuario = input('Ingrese su usuario: ').lower()
            if " " in usuario or "@" in usuario:
                raise ValueError
            elif usuario == "":
                raise ValueError
            else:                
                usuario_ok = True
        except ValueError:
            print('El usuario ingresado no es válido')

    return usuario

def obtener_contrasena():
    contrasena_ok: bool = False
    while not contrasena_ok:
        try:
            contrasena = getpass.getpass('Ingrese su contraseña: ')
            if " " in contrasena:
                raise ValueError
            elif contrasena == "":
                raise ValueError
            else:                
                contrasena_ok = True
        except ValueError:
            print('La contraseña ingresada no es válida')

    return contrasena


def iniciar_sesion(browser, usuario, contrasena):
    time.sleep(1)
    username_el = browser.find_element("name", 'username')
    password_el = browser.find_element("name", 'password')
    time.sleep(1)
    username_el.send_keys(usuario)
    time.sleep(1)
    password_el.send_keys(contrasena)
    submit_el = browser.find_element("xpath", "//button[@type='submit']")
    time.sleep(1)
    submit_el.click()
    time.sleep(7)


def main():
    followers: list = []
    usuario = obtener_usuario()
    contrasena = obtener_contrasena()
    browser = webdriver.Chrome()
    browser.get('https://www.instagram.com')
    iniciar_sesion(browser, usuario, contrasena)
    not_now_el = browser.find_element("xpath", "//button[contains(text(), 'Ahora no')]")
    not_now_el.click()
    time.sleep(5)
    not_now_el = browser.find_element("xpath", "//button[contains(text(), 'Ahora no')]")
    not_now_el.click()
    time.sleep(3)
    profile_el = browser.find_element("xpath", "//a[@href='/" + usuario + "/']")
    profile_el.click()
    time.sleep(10)
# get followers number
    followers_num_el = browser.find_element("xpath", "//a[@href='/" + usuario + "/followers/']")
    followers_num = followers_num_el.text
    followers_num = followers_num.replace("seguidores", "")
    followers_num = followers_num.replace(" ", "")
    followers_num = int(followers_num)
    followers_el = browser.find_element("xpath", "//a[@href='/" + usuario + "/followers/']")
    followers_el.click()
    # scroll slowly to load all followers until it reaches the end
    time.sleep(5)
    scroll_box = browser.find_element("xpath", "//div[@class='isgrP']")
    last_ht, ht = 0, 1
    while last_ht != ht:
        last_ht = ht
        time.sleep(1)
        ht = browser.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight); 
            return arguments[0].scrollHeight;
            """, scroll_box)
    

    time.sleep(5)
    # get followers list
    followers_list_el = browser.find_elements("xpath", "//div[@class='PZuss']/li")
    for follower_el in followers_list_el:
        follower = follower_el.text
        followers.append(follower)
# 
    with open("followers.txt", "w") as f:
        for follower in followers:
            f.write(follower + "\n")
    browser.close()
    print("Done")
    time.sleep(5)

main()