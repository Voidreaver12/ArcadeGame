#Useful functions that for the game

#Collision Detection:
#Checks two objects A and B for collision with each other
#The objects must have variables: x, y, width, height
#(x and y are used as the center of the object)
#and Functions: OnCollide(object collided with)

def CheckCollide(A,B):
    if ((A.x< B.x + B.width) and
        (A.x+A.width > B.x) and
        (A.y < B.y + B.height) and
        (A.y+A.height > B.y)):
        #collsion detected, OnCollide called on both objects
        try:
            A.OnCollide(B)
        except:
            print(A, "has no collision defined")
        try:
            B.OnCollide(A)
        except:
            print(B, "has no collision defined")

    
