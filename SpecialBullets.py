import ship as g

class BounceBullet:
    def __init__(self, x, y, vx, vy):
        g.Bullet.__init__(self,x, y, vx, vy)
    def update(self):
        g.Bullet.update(self)
        if (self.x < 0 or self.x > WINDOW_W):
            self.xv = self.xv*-1
