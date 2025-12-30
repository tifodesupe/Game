import arcade
import time
import random
from constantes import (
    ALTO_PANTALLA,
    ANCHO_PANTALLA, 
    TITULO,
    GRAVEDAD,
    VELOCIDAD_SALTO,
    TILE_SCALING
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
        self.monedas = None
        self.puntuacion = None
        self.camara_juego = None
        self.camara_gui = None

    def setup(self):
        """Configura el juego, llamar para iniciar o reiniciar"""
        #Crear el sprite del jugador
        #El sprite del jugador (se inicializa en setup)
        self.jugador_lista = arcade.SpriteList()
        self.jugador = JugadorAnimado()
        #Plataformas sin sprites
        """self.plataformas = arcade.SpriteList(use_spatial_hash=True)
        suelo = arcade.SpriteSolidColor(
            ANCHO_PANTALLA,
            40,
            arcade.color.DARK_BROWN
        )
        suelo.center_x = ANCHO_PANTALLA // 2
        suelo.center_y = 20
        self.plataformas.append(suelo)"""

        self.camara_juego = arcade.Camera2D()
        self.camara_gui = arcade.Camera2D()

        self.jugador.center_x = ANCHO_PANTALLA // 2
        self.jugador.center_y = ALTO_PANTALLA // 2
        self.jugador_lista.append(self.jugador)
        self.puntuacion = 0



        layer_options = {
            "Plataformas": {
                "use_spatial_hash": True  # Optimiza colisiones
            },
            "Monedas": {
                "use_spatial_hash": True
            }
        }
        
        # Cargar el mapa de Tiled
        self.tile_map = arcade.load_tilemap(
            "assets/maps/level_1.tmx",
            scaling=TILE_SCALING,
            layer_options=layer_options
        )
        
        # Extraer las capas como SpriteLists
        self.plataformas = self.tile_map.sprite_lists["Plataformas"]
        self.monedas = self.tile_map.sprite_lists["Monedas"]
        for moneda in self.monedas:
            print("Moneda:", moneda)
        self.fondo = self.tile_map.sprite_lists.get("Fondo", arcade.SpriteList())
        
        # Color de fondo del mapa (si se definió en Tiled)
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        
        self.motor_fisica = arcade.PhysicsEnginePlatformer(
            player_sprite=self.jugador,    # El sprite del jugador
            walls=self.plataformas,        # Plataformas y suelo
            gravity_constant= GRAVEDAD      # Fuerza de gravedad
        )
        self.jugador.set_motor_fisica(self.motor_fisica)

    def centrar_camara_en_jugador(self):
        """Centrar camara en el jugador"""
        posicion_objetivo = (self.jugador.center_x, self.jugador.center_y)
        
        self.camara_juego.position = arcade.math.lerp_2d(
            self.camara_juego.position, 
            posicion_objetivo, 
            0.1
        )


    def on_draw(self):
        """Dibuja todo en la pantalla"""
        self.clear()
        # 1. Activar cámara del juego (lo que se mueve)
        self.camara_juego.use()
    
        # 2. Dibujar elementos del mundo (se verán afectados por la cámara)
        self.fondo.draw()
        self.plataformas.draw()
        self.monedas.draw()
        self.jugador_lista.draw()
        self.jugador_lista.draw_hit_boxes()
        # self.jugador.draw_hit_box() # Opcional: solo para pruebas

        # 3. Activar cámara GUI (lo que está fijo en la pantalla)
        self.camara_gui.use()
    
        # 4. Dibujar elementos de interfaz (siempre visibles en la misma esquina)
        arcade.draw_text(
            f"Puntos: {self.puntuacion}",
            20,                         # Margen izquierdo
            ALTO_PANTALLA - 40,           # Margen superior
            arcade.color.WHITE,
            20
        )

    def on_key_press(self, tecla, modificadores):
        ###print("Se oprimió la tecla:", tecla)
        self.jugador.mover(tecla)
    
    def on_key_release(self, tecla, modificadores):
        """Se ejecuta cuando se suelta una tecla."""
        self.jugador.liberar_tecla(tecla)

    def on_update(self, delta_time):
        self.motor_fisica.update()  
        self.jugador_lista.update()
        self.jugador.update_animation(delta_time)
        monedas_tocadas = arcade.check_for_collision_with_list(
            self.jugador, self.monedas
        )
        self.centrar_camara_en_jugador()  # Actualizar cámara
        self.monedas.update()
        
        for moneda in monedas_tocadas:
            moneda.remove_from_sprite_lists()
            self.puntuacion += 10
            # Aquí podrías reproducir un sonido


def main():
    """Función principal del juego"""
    juego = MiJuego()
    juego.setup()
    arcade.run()


if __name__ == "__main__":
    main()