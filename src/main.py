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



class MiJuego(arcade.View):
    """Ventana principal del juego"""
    def __init__ (self):
        """Inicializa la ventana del juego"""
        super().__init__()
        ###arcade.set_background_color (arcade.color.CORNFLOWER_BLUE)
        self.jugador_lista = None
        self.jugador = None
        self.motor_fisica = None
        self.plataformas = None
        self.monedas = None
        self.puntuacion = None
        self.camara_juego = None
        self.camara_gui = None
        self.vidas = None
        
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.camara_juego = arcade.Camera2D(self.window)
        self.camara_gui = arcade.Camera2D(self.window)

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

        self.camara_juego = arcade.Camera2D(self.window)
        self.camara_gui = arcade.Camera2D(self.window)


        self.jugador.center_x = ANCHO_PANTALLA // 2
        self.jugador.center_y = ALTO_PANTALLA // 2
        self.jugador_lista.append(self.jugador)
        self.puntuacion = 0
        self.vidas = 5



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
        if tecla == arcade.key.ESCAPE:
            # Ir a pausa, pasando referencia a esta vista
            pause = PauseView(self)
            self.show_view(pause)
    
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
        if self.vidas <= 0:
            game_over = GameOverView(self.score)
            self.window.show_view(game_over)


class MenuView(arcade.View):
    """Vista del menú principal."""

    def on_show_view(self):
        """Se ejecuta cuando esta vista se activa (equivalente a enter())."""
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        """Dibuja el menú."""
        self.clear()
        arcade.draw_text(
            "MI PLATAFORMERO",
            ANCHO_PANTALLA / 2,
            ALTO_PANTALLA / 2 + 50,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center"
        )
        arcade.draw_text(
            "Presiona ENTER para jugar",
            ANCHO_PANTALLA / 2,
            ALTO_PANTALLA / 2 - 30,
            arcade.color.LIGHT_GRAY,
            font_size=20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        """Maneja las teclas presionadas."""
        if key == arcade.key.ENTER:
            # Transición al estado de juego
            game_view = MiJuego()
            self.window.show_view(game_view)
            game_view.setup()

    
class PauseView(arcade.View):
    """Vista de pausa. Guarda referencia al juego para volver."""

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view  # Guardamos referencia al juego

    def on_draw(self):
        """Dibuja la pantalla de pausa."""
        # Primero dibujamos el juego de fondo (congelado)
        self.game_view.on_draw()

        self.game_view.camara_gui.use()

        arcade.draw_lrbt_rectangle_filled(
            0,
            ANCHO_PANTALLA //2,
            0,
            0,
            (0, 0, 0, 128)
        )
        # Texto de pausa
        arcade.draw_text(
            "PAUSA",
            ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2 + 50,
            arcade.color.WHITE, font_size=50, anchor_x="center"
        )
        arcade.draw_text(
            "Presiona ESCAPE para continuar",
            ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2 - 20,
            arcade.color.WHITE, font_size=20, anchor_x="center"
        )
        arcade.draw_text(
            "Presiona Q para volver al menú",
            ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2 - 60,
            arcade.color.WHITE, font_size=20, anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        """Maneja las teclas en pausa."""
        if key == arcade.key.ESCAPE:
            # Volver al juego (la misma instancia)
            self.window.show_view(self.game_view)
        elif key == arcade.key.Q:
            # Volver al menú (nueva instancia)
            menu = MenuView()
            self.window.show_view(menu)
    
class GameOverView(arcade.View):
    """Vista de fin del juego."""

    def __init__(self, score):
        super().__init__()
        self.score = score

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_RED)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "GAME OVER",
            ALTO_PANTALLA / 2,  ALTO_PANTALLA / 2 + 50,
            arcade.color.WHITE, font_size=50, anchor_x="center"
        )
        arcade.draw_text(
            f"Puntuación final: {self.score}",
            ALTO_PANTALLA / 2,  ALTO_PANTALLA / 2,
            arcade.color.WHITE, font_size=25, anchor_x="center"
        )
        arcade.draw_text(
            "Presiona ENTER para volver al menú",
            ALTO_PANTALLA / 2,  ALTO_PANTALLA / 2 - 50,
            arcade.color.WHITE, font_size=20, anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            menu = MenuView()
            self.window.show_view(menu)




def main():
    """Función principal del juego
    juego = MiJuego()
    juego.setup()
    arcade.run()"""

    window = arcade.Window(ANCHO_PANTALLA, ALTO_PANTALLA, TITULO)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()