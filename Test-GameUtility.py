#this file tests the GameUtility functions
import GameUtility

#classes used to test collsion function
class TestBox:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def OnCollide(self,hit):
        print("Pass")
    def __str__(self):
        return "TestBox"

class TestBoxUnd:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def __str__(self):
        return "This should have no collsion defined..."
#the collsion tests
print("Collision Tests:")

#tests upper right collision        
box1 = TestBox(0,0,6,6)
box2 = TestBox(5,5,6,6)
print("Next two lines should be pass:")
CheckCollide(box1,box2)
print("")

#lower left collision
box1 = TestBox(0,0,6,6)
box2 = TestBox(-5,-5,6,6)
print("Next two lines should be pass:")
CheckCollide(box1,box2)
print("")

#tests bare miss for no collision
box1 = TestBox(0,0,2,2)
box2 = TestBox(0,2,2,2)
print("Next line should be ***:")
CheckCollide(box1,box2)
print("***")
print("")

#tests no collision
box1 = TestBox(0,0,3,3)
box2 = TestBox(5,5,3,3)
print("Next line should be ***:")
CheckCollide(box1,box2)
print("***")
print("")

#test undefined collision error
box1 = TestBoxUnd(0,0,6,6)
box2 = TestBox(5,5,6,6)
print("Should have one undefined and one pass:")
CheckCollide(box1,box2)
print("")

print("Done testing collision")
print("")
