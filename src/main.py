import arcade
import player

#constantes del juego

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
VELOCIDAD_MOVIMIENTO = 5

TITULO = "Mi primer juego"

class MiJuego(arcade.Window):
    """Ventana principal del juego"""
    def __init__ (self):
        """Inicializa la ventana del juego"""
        super().__init__(ANCHO_PANTALLA, ALTO_PANTALLA, TITULO)
        arcade.set_background_color (arcade.color.AMAZON)
        #Posicion del jugador
        self.jugador_x = 400
        self.jugador_y = 300
        #Velocidad del jugador
        self.velocidad_x = 0
        self.velocidad_y = 0

    
    def on_draw(self):
        """Dibuja todo en la pantalla"""
        self.clear()
        arcade.draw_circle_filled(
            self.jugador_x, self.jugador_y, 25, arcade.color.BLUE
        )

    def on_update(self, delta_time):
        """Actualiza la lógica del juego"""
        self.jugador_x +=self.velocidad_x
        self.jugador_y += self.velocidad_y

        if self.jugador_x > ANCHO_PANTALLA:
            self.jugador_x = ANCHO_PANTALLA
        if self.jugador_x < 0:
            self.jugador_x = 0
        if self.jugador_y < 0:
            self.jugador_y = 0
        if self.jugador_y > ALTO_PANTALLA:
            self.jugador_y = ALTO_PANTALLA
        
    
    def on_key_press(self, tecla, modificadores):
        """Se ejecuta cuando se preciona una telca"""
        if tecla == arcade.key.UP or tecla == arcade.key.W:
            self.velocidad_y = VELOCIDAD_MOVIMIENTO
        elif tecla == arcade.key.DOWN or tecla == arcade.key.S:
            self.velocidad_y = -VELOCIDAD_MOVIMIENTO
        elif tecla == arcade.key.LEFT or tecla == arcade.key.A:
            self.velocidad_x = -VELOCIDAD_MOVIMIENTO
        elif tecla == arcade.key.RIGHT or tecla == arcade.key.D:
            self.velocidad_x = VELOCIDAD_MOVIMIENTO
    
    def on_key_release(self, tecla, modificadores):
        """Se ejecuta cuanto se suelta una tecla"""
        if tecla in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.velocidad_y = 0
            self.velocidad_x = 0
        if tecla in (arcade.key.W, arcade.key.S, arcade.key.A, arcade.key.D):
            self.velocidad_y = 0
            self.velocidad_x = 0
        



def main():
    """Función principal del juego"""
    juego = MiJuego()
    arcade.run()

if __name__ == "__main__":
    main()