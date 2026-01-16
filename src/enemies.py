import arcade
from constantes import(
    TILE_SCALING
)


class EnemigoAnimado(arcade.AnimatedWalkingSprite):
    def __init__(self):
        super().__init__()
        self.scale = TILE_SCALING * 3
        self.tiempo_transcurrido = 0
        self.frame_actual = 0
        self.tiempo_entre_frames = 0.1
        self.direccion = "idle"
        self.texturas_idle = [
            arcade.load_texture("assets/images/enemy/LightBandit_idle_0.png"),
            arcade.load_texture("assets/images/enemy/LightBandit_idle_1.png"),
            arcade.load_texture("assets/images/enemy/LightBandit_idle_2.png"),
            arcade.load_texture("assets/images/enemy/LightBandit_idle_3.png")
        ]
        self.texturas_caminar_derecha = [
            arcade.load_texture("assets/images/enemy/LightBandit_run_0.png"),
            arcade.load_texture("assets/images/enemy/LightBandit_run_1.png"),
            arcade.load_texture("assets/images/enemy/LightBandit_run_2.png"),
            arcade.load_texture("assets/images/enemy/LightBandit_run_3.png"),
            arcade.load_texture("assets/images/enemy/LightBandit_run_4.png"),
            arcade.load_texture("assets/images/enemy/LightBandit_run_5.png"),
            arcade.load_texture("assets/images/enemy/LightBandit_run_6.png"),
            arcade.load_texture("assets/images/enemy/LightBandit_run_7.png")

        ]
        self.texturas_caminar_izquierda = [
            arcade.load_texture("assets/images/enemy/LightBandit_runl_left_0.png", ),
            arcade.load_texture("assets/images/enemy/LightBandit_runl_left_1.png", ),
            arcade.load_texture("assets/images/enemy/LightBandit_runl_left_2.png", ),
            arcade.load_texture("assets/images/enemy/LightBandit_runl_left_3.png", ),
            arcade.load_texture("assets/images/enemy/LightBandit_runl_left_4.png", ),
            arcade.load_texture("assets/images/enemy/LightBandit_runl_left_5.png", ),
            arcade.load_texture("assets/images/enemy/LightBandit_runl_left_6.png", ),
            arcade.load_texture("assets/images/enemy/LightBandit_runl_left_7.png", )

        ]
        self.texture = self.texturas_idle[0]


    def update_animation(self, delta_time):
        if self.change_x > 0:
            self.direccion = "izquierda"
        elif self.change_x < 0:
            self.direccion = "derecha"
        else:
            self.direccion = "idle"
        
                

        self.tiempo_transcurrido += delta_time

        if self.tiempo_transcurrido >= self.tiempo_entre_frames:
            self.tiempo_transcurrido = 0
            self.frame_actual += 1

        if self.direccion == "derecha":
            self.frame_actual %= len(self.texturas_caminar_derecha)
            self.texture = self.texturas_caminar_derecha[self.frame_actual]

        elif self.direccion == "izquierda":
            self.frame_actual %= len(self.texturas_caminar_izquierda)
            self.texture = self.texturas_caminar_izquierda[self.frame_actual]

        else:
            self.frame_actual %= len(self.texturas_idle)
            self.texture = self.texturas_idle[self.frame_actual]
        