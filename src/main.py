import arcade
import time
import random
from constantes import (
    ALTO_PANTALLA,
    ANCHO_PANTALLA, 
    TITULO, 
    RUTA_MONEDA, 
    ESCALA_MONEDA,
    TIME_OUT
)
from player import JugadorAnimado

#constantes del juego



class MiJuego(arcade.Window):
    """Ventana principal del juego"""
    def __init__ (self):
        """Inicializa la ventana del juego"""
        super().__init__(ANCHO_PANTALLA, ALTO_PANTALLA, TITULO)
        arcade.set_background_color (arcade.color.CORNFLOWER_BLUE)
        self.monedas_lista = None
        self.jugador_lista = None
        self.jugador = None
        self.puntuacion = None
        self.tiempo_inicio = None

    def setup(self):
        """Configura el juego, llamar para iniciar o reiniciar"""
        #Crear el sprite del jugador
        #El sprite del jugador (se inicializa en setup)
        self.monedas_lista = arcade.SpriteList()
        self.jugador_lista = arcade.SpriteList()
        self.jugador = JugadorAnimado()
        self.puntuacion = 0
        self.tiempo_inicio = time.time()
    

        self.jugador.center_x = ANCHO_PANTALLA // 2
        self.jugador.center_y = ALTO_PANTALLA // 2
        self.jugador_lista.append(self.jugador)
        self.dibujar_monedas()

    def dibujar_monedas(self):
        for _ in range(10):
            moneda = arcade.Sprite(RUTA_MONEDA, ESCALA_MONEDA)
            moneda.center_x = random.randint(50, ANCHO_PANTALLA - 50)
            moneda.center_y = random.randint(50, ALTO_PANTALLA - 50)
            self.monedas_lista.append(moneda)


    def on_draw(self):
        """Dibuja todo en la pantalla"""
        if self.tiempo_restante() < 0:
            return
        self.clear()
        self.jugador_lista.draw()
        self.jugador.draw_hit_box()
        self.monedas_lista.draw()
        arcade.draw_text(
            f"Puntuación: {self.puntuacion}",
            10,  # posición x
            ALTO_PANTALLA - 30,  # posición y
            arcade.color.BLACK,  # color
            18,  # tamaño de fuente
            font_name="Arial"
        )
        arcade.draw_text(
            f"Tiempo: {self.tiempo_restante()}",
            10,  # posición x
            ALTO_PANTALLA - 60,  # posición y
            arcade.color.BLACK,  # color
            18,  # tamaño de fuente
            font_name="Arial"
        )

    def on_key_press(self, tecla, modificadores):
        print("Se oprimió la tecla:", tecla)
        self.jugador.mover(tecla)
    
    def on_key_release(self, tecla, modificadores):
        """Se ejecuta cuando se suelta una tecla."""
        self.jugador.liberar_tecla(tecla)

    def on_update(self, delta_time):
        if self.tiempo_restante() < 0:
            self.clear()
            self.jugador_lista = None
            arcade.draw_text(
                f"Fin: {self.puntuacion} puntos",
                10,  # posición x
                ALTO_PANTALLA - 30,  # posición y
                arcade.color.BLACK,  # color
                18,  # tamaño de fuente
                font_name="Arial"
            )
            return

        self.monedas_lista.update()

        monedas_tocadas = arcade.check_for_collision_with_list(
        self.jugador, self.monedas_lista
        )
        self.jugador_lista.update()
        self.jugador.update_animation(delta_time)
        # Procesar cada moneda tocada
        for moneda in monedas_tocadas:
            moneda.remove_from_sprite_lists()
            self.puntuacion += 10
        
        if len(self.monedas_lista) == 0:
            self.dibujar_monedas()


    def tiempo_restante(self):
        return int(self.tiempo_inicio + TIME_OUT - time.time())

def main():
    """Función principal del juego"""
    juego = MiJuego()
    juego.setup()
    arcade.run()


if __name__ == "__main__":
    main()