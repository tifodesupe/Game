import arcade
import time
import random
from constantes import (
    ALTO_PANTALLA,
    ANCHO_PANTALLA, 
    TITULO,
    GRAVEDAD,
    VELOCIDAD_SALTO
)
from player import JugadorAnimado
#constantes del juego



class MiJuego(arcade.Window):
    """Ventana principal del juego"""
    def __init__ (self):
        """Inicializa la ventana del juego"""
        super().__init__(ANCHO_PANTALLA, ALTO_PANTALLA, TITULO)
        arcade.set_background_color (arcade.color.CORNFLOWER_BLUE)
        self.jugador_lista = None
        self.jugador = None
        self.motor_fisica = None
        self.plataformas = None
        self.tile_map = None

    def setup(self):
        """Configura el juego, llamar para iniciar o reiniciar"""
        #Crear el sprite del jugador
        #El sprite del jugador (se inicializa en setup)
        self.jugador_lista = arcade.SpriteList()
        self.jugador = JugadorAnimado()
        self.plataformas = arcade.SpriteList(use_spatial_hash=True)
        suelo = arcade.SpriteSolidColor(
            ANCHO_PANTALLA,
            40,
            arcade.color.DARK_BROWN
        )
        suelo.center_x = ANCHO_PANTALLA // 2
        suelo.center_y = 20
        self.plataformas.append(suelo)
    

        self.jugador.center_x = ANCHO_PANTALLA // 2
        self.jugador.center_y = ALTO_PANTALLA // 2
        self.jugador_lista.append(self.jugador)
        self.motor_fisica = arcade.PhysicsEnginePlatformer(
            player_sprite=self.jugador,    # El sprite del jugador
            walls=self.plataformas,        # Plataformas y suelo
            gravity_constant= GRAVEDAD      # Fuerza de gravedad
        )
        self.jugador.set_motor_fisica(self.motor_fisica)        


    def on_draw(self):
        """Dibuja todo en la pantalla"""
        self.clear()
        self.plataformas.draw()
        self.jugador_lista.draw()
        self.jugador.draw_hit_box()
    

    def on_key_press(self, tecla, modificadores):
        print("Se oprimió la tecla:", tecla)
        self.jugador.mover(tecla)
    
    def on_key_release(self, tecla, modificadores):
        """Se ejecuta cuando se suelta una tecla."""
        self.jugador.liberar_tecla(tecla)

    def on_update(self, delta_time):
        self.clear()
        self.motor_fisica.update()  
        self.jugador_lista.update()
        self.jugador.update_animation(delta_time)


def main():
    """Función principal del juego"""
    juego = MiJuego()
    juego.setup()
    arcade.run()


if __name__ == "__main__":
    main()