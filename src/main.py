import arcade

#constantes del juego

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
RUTA_JUGADOR = "assets/images/player/necromancer_anim_f2.png"
# Escala del sprite (1.0 = tamaño original)
ESCALA_DEL_JUGADOR = 3
VELOCIDAD_DE_MOVIMIENTO = 5
TITULO = "Juego con sprites"

class MiJuego(arcade.Window):
    """Ventana principal del juego"""
    def __init__ (self):
        """Inicializa la ventana del juego"""
        super().__init__(ANCHO_PANTALLA, ALTO_PANTALLA, TITULO)
        arcade.set_background_color (arcade.color.CORNFLOWER_BLUE)

    def setup(self):
        """Configura el juego, llamar para iniciar o reiniciar"""
        #Crear el sprite del jugador
        #El sprite del jugador (se inicializa en setup)
        self.jugador = Jugador()
    

        self.jugador.center_x = ANCHO_PANTALLA // 2
        self.jugador.center_y = ALTO_PANTALLA // 2
        print("Tecla arriba:", arcade.key.UP)
        print("Tecla abajo:", arcade.key.DOWN)
        print("Tecla izquierda:", arcade.key.LEFT)
        print("Tecla derecha:", arcade.key.RIGHT)
        print("Tecla W:", arcade.key.W)
        print("Tecla S:", arcade.key.S)
        print("Tecla A:", arcade.key.A)
        print("Tecla D:", arcade.key.D)


    def on_draw(self):
        """Dibuja todo en la pantalla"""
        self.clear()
        arcade.draw.draw_sprite(self.jugador)
        self.jugador.draw_hit_box()

    def on_key_press(self, tecla, modificadores):
        print("Se oprimió la tecla:", tecla)
        self.jugador.mover(tecla)
    
    def on_key_release(self, tecla, modificadores):
        """Se ejecuta cuando se suelta una tecla."""
        self.jugador.liberar_tecla(tecla)

    def on_update(self, delta_time):
        self.jugador.update()

class Jugador(arcade.Sprite):
    def __init__(self):
        super().__init__(RUTA_JUGADOR, ESCALA_DEL_JUGADOR)

        # Velocidad del jugador
        self.change_x = 0
        self.change_y = 0

    def mover(self, tecla):
        if tecla == arcade.key.UP or tecla == arcade.key.W:
            self.change_y = VELOCIDAD_DE_MOVIMIENTO
        if tecla == arcade.key.DOWN or tecla == arcade.key.S:
            self.change_y = -VELOCIDAD_DE_MOVIMIENTO
        if tecla == arcade.key.LEFT or tecla == arcade.key.A:
            self.change_x = -VELOCIDAD_DE_MOVIMIENTO
        if tecla == arcade.key.RIGHT or tecla == arcade.key.D:
            self.change_x = VELOCIDAD_DE_MOVIMIENTO

    def liberar_tecla(self, tecla):
        print("Se liberó la tecla:", tecla)
        if tecla in (arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S):
            self.change_y = 0
        elif tecla in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.change_x = 0
    
    def update(self):
        super().update()

        if self.left < 0:
            self.left = 0

        if self.right > ANCHO_PANTALLA:
            self.right = ANCHO_PANTALLA
        
        if self.bottom < 0:
            self.bottom = 0
        
        if self.top > ALTO_PANTALLA:
            self.top = ALTO_PANTALLA

    


def main():
    """Función principal del juego"""
    juego = MiJuego()
    juego.setup()
    arcade.run()


if __name__ == "__main__":
    main()