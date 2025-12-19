import arcade
from constantes import(
    RUTA_JUGADOR, 
    ESCALA_DEL_JUGADOR,
    VELOCIDAD_DE_MOVIMIENTO,
    ALTO_PANTALLA,
    ANCHO_PANTALLA,
    VELOCIDAD_SALTO
)


class Jugador(arcade.Sprite):
    def __init__(self):
        super().__init__(RUTA_JUGADOR, ESCALA_DEL_JUGADOR)

        # Velocidad del jugador
        self.change_x = 0
        self.change_y = 0
        self.texturas_idle = []
        self.texturas_caminar_derecha = []
        self.texturas_caminar_izquierda = []
        self.motor_fisica = None
    
    def set_motor_fisica(self, motor):
        self.motor_fisica = motor

    def mover(self, tecla,):
        if tecla in (arcade.key.SPACE, arcade.key.UP):
            if self.motor_fisica and self.motor_fisica.can_jump():
                self.change_y = VELOCIDAD_SALTO
        if tecla == arcade.key.LEFT or tecla == arcade.key.A:
            self.change_x = -VELOCIDAD_DE_MOVIMIENTO
        if tecla == arcade.key.RIGHT or tecla == arcade.key.D:
            self.change_x = VELOCIDAD_DE_MOVIMIENTO

    def liberar_tecla(self, tecla):
        print("Se liberó la tecla:", tecla)
        if tecla in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.change_x = 0
    
    def update(self, delta_time):
        super().update(delta_time)

        if self.left < 0:
            self.left = 0

        if self.right > ANCHO_PANTALLA:
            self.right = ANCHO_PANTALLA
        
        if self.bottom < 0:
            self.bottom = 0
        
        if self.top > ALTO_PANTALLA:
            self.top = ALTO_PANTALLA

class JugadorAnimado(Jugador):
    def __init__(self):
        super().__init__()

        self.texturas_idle = []
        self.texturas_caminar_derecha = []
        self.texturas_caminar_izquierda = []
        # Cargar idle
        self.texturas_idle.append(arcade.load_texture("assets/images/player/idle.png"))

         # Cargar frames de caminar derecha
        for i in range(1, 3):
            textura = arcade.load_texture(f"assets/images/player/caminar_derecha_{i}.png")
            self.texturas_caminar_derecha.append(textura)
        
        # Cargar frames de caminar izquierda
        for i in range(1, 3):
            textura = arcade.load_texture(f"assets/images/player/caminar_izquierda_{i}.png")
            self.texturas_caminar_izquierda.append(textura)

        # Estado de la animación
        self.frame_actual = 0
        self.tiempo_entre_frames = 0.1  # segundos
        self.tiempo_transcurrido = 0
        self.direccion = 'idle'

        # Establecer textura inicial
        self.texture = self.texturas_idle[0]
        self.scale = ESCALA_DEL_JUGADOR

    def update_animation(self, delta_time):
        """Actualiza la animación basándose en el movimiento."""
        # Determinar dirección basándose en velocidad
        if self.change_x > 0:
            self.direccion = 'derecha'
        elif self.change_x < 0:
            self.direccion = 'izquierda'
        else:
            self.direccion = 'idle'
        
        # Actualizar tiempo
        self.tiempo_transcurrido += delta_time
        
        # ¿Es hora de cambiar de frame?
        if self.tiempo_transcurrido >= self.tiempo_entre_frames:
            self.tiempo_transcurrido = 0
            self.frame_actual += 1
            
            # Seleccionar la textura correcta
            if self.direccion == 'derecha':
                self.frame_actual %= len(self.texturas_caminar_derecha)
                self.texture = self.texturas_caminar_derecha[self.frame_actual]
            elif self.direccion == 'izquierda':
                self.frame_actual %= len(self.texturas_caminar_izquierda)
                self.texture = self.texturas_caminar_izquierda[self.frame_actual]
            else:
                self.frame_actual = 0
                self.texture = self.texturas_idle[0]
            
    