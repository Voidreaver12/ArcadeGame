#Useful functions that for the game

#Collision Detection:
#Checks two objects A and B for collision with each other
#The objects must have variables: x, y, width, height
#(x and y are used as the center of the object)
#and Functions: OnCollide(object collided with)

def CheckCollide(A,B):
    if ((A.x-A.width/2 < B.x + B.width/2) and
        (A.x+A.width/2 > B.x - B.width/2) and
        (A.y-A.width/2 < B.y + B.width/2) and
        (A.y+A.width/2 > B.y - B.width/2)):
        #collsion detected, OnCollide called on both objects
        try:
            A.OnCollide(B)
        except:
            print(A, "has no collision defined")
        try:
            B.OnCollide(A)
        except:
            print(B, "has no collision defined")

    
