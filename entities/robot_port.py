import math


class LogisticRobot:
    SPEED = 4.0

    def __init__(self, home_port):
        self.home   = home_port
        self.x      = float(home_port.x)
        self.y      = float(home_port.y)
        self.cargo: str | None = None
        self.target = None
        self.charge = 1.0
        self.state  = "idle"
        self._src   = None

    def update(self, dt: float, ports: list) -> None:
        if self.charge <= 0.05:
            self._go_home(dt)
            self.charge = min(1.0, self.charge + dt * 0.2)
            self.state  = "charging"
            return
        if self.state == "idle":
            self._find_task(ports)
        elif self.state in ("fetching", "delivering"):
            self._move(dt)
        self.charge = max(0.0, self.charge - dt * 0.02)

    def _find_task(self, ports):
        for port in ports:
            if port is self.home:
                continue
            if port.output_buffer:
                self.target = (port.x, port.y)
                self._src   = port
                self.state  = "fetching"
                return

    def _move(self, dt):
        if self.target is None:
            self.state = "idle"
            return
        tx, ty = self.target
        dx, dy = tx - self.x, ty - self.y
        dist = math.hypot(dx, dy)
        if dist < 0.15:
            self._arrive()
            return
        step = self.SPEED * dt
        r    = step / dist
        self.x += dx * r
        self.y += dy * r

    def _arrive(self):
        if self.state == "fetching":
            if self._src and self._src.output_buffer:
                self.cargo = self._src.output_buffer.pop(0)
            self.target = (self.home.x, self.home.y)
            self.state  = "delivering"
        elif self.state == "delivering":
            if self.cargo:
                self.home.input_buffer.append(self.cargo)
                self.cargo = None
            self.state = "idle"

    def _go_home(self, dt):
        self.target = (self.home.x, self.home.y)
        self._move(dt)


class RobotPort:
    btype    = "robot_port"
    MAX_BOTS = 5

    def __init__(self, x: int, y: int):
        self.x              = x
        self.y              = y
        self.output_buffer: list[str] = []
        self.input_buffer:  list[str] = []
        self.robots: list[LogisticRobot] = []
        self.powered = True
        self.status  = "idle"

    def spawn_robots(self):
        while len(self.robots) < self.MAX_BOTS:
            self.robots.append(LogisticRobot(self))

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return
        self.spawn_robots()
        all_ports = [b for b in gmap.buildings if b.btype == "robot_port"]
        for robot in self.robots:
            robot.update(dt, all_ports)
        self.status = "working" if any(r.state != "idle" for r in self.robots) else "idle"

    def accept_item(self, item: str, _from=None) -> bool:
        self.output_buffer.append(item)
        return True

    def serialize(self) -> dict:
        return {
            "type": "robot_port", "x": self.x, "y": self.y,
            "output_buffer": self.output_buffer, "input_buffer": self.input_buffer,
        }