import arcade

#constantes del juego

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
RUTA_JUGADOR = "assets/images/player/necromancer_anim_f2.png"
# Escala del sprite (1.0 = tamaño original)
ESCALA_DEL_JUGADOR = 0.5
TITULO = "Juego con sprites"

class MiJuego(arcade.Window):
    """Ventana principal del juego"""
    def __init__ (self):
        """Inicializa la ventana del juego"""
        super().__init__(ANCHO_PANTALLA, ALTO_PANTALLA, TITULO)
        arcade.set_background_color (arcade.color.CORNFLOWER_BLUE)

        #El sprite del jugador (se inicializa en setup)
        self.jugador = None
    
    def setup(self):
        """Configura el juego, llamar para iniciar o reiniciar"""
        #Crear el sprite del jugador
        self.jugador = arcade.Sprite(RUTA_JUGADOR, ESCALA_DEL_JUGADOR)
        self.jugador.center_x = ANCHO_PANTALLA // 2
        self.jugador.center_y = ALTO_PANTALLA // 2



    
    def on_draw(self):
        """Dibuja todo en la pantalla"""
        self.clear()
        self.jugador.draw_hit_box()



def main():
    """Función principal del juego"""
    juego = MiJuego()
    juego.setup()
    arcade.run()


if __name__ == "__main__":
    main()