import arcade
import player

#constantes del juego

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

Titulo = "Mi primer juego"

class MiJuego(arcade.Window):
    """Ventana principal del juego"""
    def __init__ (self):
        """Inicializa la ventana del juego"""
        super().__init__(ANCHO_PANTALLA, ALTO_PANTALLA, Titulo)
        arcade.set_background_color (arcade.color.AMAZON)
    
    def on_draw(self):
        """Dibuja todo en la pantalla"""
        self.clear()

        #Dibujar un círculo
        arcade.draw_circle_filled(300, 400, 50, arcade.color.YELLOW)
        #Dibujar un rectangulo
        arcade.draw_lbwh_rectangle_filled(200, 200, 100, 50, arcade.color.RED)
        #Dibujar una línea
        arcade.draw_line(0, 0, 800, 600, arcade.color.BLUE)
        #Dibujar texto
        arcade.draw_text("Hola mundo", 300, 500, arcade.color.BLACK, 24)


def main():
    """Función principal del juego"""
    juego = MiJuego()
    arcade.run()

if __name__ == "__main__":
    main()