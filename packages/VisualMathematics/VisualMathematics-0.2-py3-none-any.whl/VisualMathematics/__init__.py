import turtle
import math
from mpmath import mp
import keyboard

def Fibonacci():

    Fib_ = turtle.Screen()
    print("The Fibonacci sequence was first found by an Italian named Leonardo Pisano Bogollo (Fibonacci). The Fibonacci sequence is a sequence of whole numbers: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ... This is an infinite sequence that starts with 0 and 1 and each term is the sum of the two preceding terms. This sequence has been termed nature's secret code.We can spot the Fibonacci sequence in the spiral patterns of sunflowers, daisies, broccoli, cauliflowers, and seashells. Let us learn more about it and its interesting properties. scource: https://www.cuemath.com/numbers/fibonacci-sequence/")

    
    Fib_screen = turtle.Screen()
    Fib_screen.title("Fibonacci")
    Fib_screen.tracer(0, 0)
    Fib_screen.setup(500, 500)
    Fib_screen.bgcolor("#ffffff")

    Fib_t = turtle.Turtle()
    Fib_j = 0
    Fib_side_length = 0.5
    Fib_fibonacci = []
    Fib_fibonacci.append(0)
    Fib_repititions = 25
    Fib_t.forward(Fib_side_length)
    Fib_t.left(90)
    Fib_t.forward(Fib_side_length)
    Fib_t.left(90)
    Fib_t.forward(Fib_side_length)
    Fib_t.left(90)
    Fib_t.forward(Fib_side_length)
    Fib_screen.update()
    for Fib_i in range(Fib_repititions):
        Fib_t.pencolor("white")
        Fib_colors = ["#89CFF0", "#7393B3", "#0096FF","#6495ED","#00A36C"]
        Fib_j += 1
        if Fib_j >= len(Fib_colors):
            Fib_j = 0
        Fib_t.fillcolor(Fib_colors[Fib_j])
    
       
        Fib_t.begin_fill()
        Fib_t.backward(Fib_side_length)
        Fib_screen.update()
   
        Fib_fibonacci.append(Fib_side_length)
        Fib_side_length = Fib_side_length + Fib_fibonacci[-2]
          
        Fib_t.right(90)
        Fib_t.forward(Fib_side_length)
        Fib_screen.update()
    
        Fib_t.left(90)
        Fib_t.forward(Fib_side_length)
        Fib_screen.update()
        Fib_t.left(90)
        Fib_t.forward(Fib_side_length)
        Fib_t.end_fill()
   
        Fib_screen.update()
    Fib_screen.mainloop() 
    turtle.done()
def infiniteTriangle():
    inf_t = turtle.Turtle()
    inf_ = turtle.Screen()
    print("Doesnt that look interesting? You can fit endless triangles in one triangle. How many can you find?")
    inf_j = 0
    inf_repitition = 8
    inf_side_length_a = 250
    inf_t.forward(inf_side_length_a)
    inf_t.left(90)
    inf_t.forward(inf_side_length_a)
    inf_side_length_c = math.sqrt(2)*inf_side_length_a
    inf_t.left(135)
    inf_t.forward(inf_side_length_c)
    inf_t.left(135)
    inf_t.forward(inf_side_length_a)
    inf_t.left(135)
    inf_.update()
    for c in range(inf_repitition):
        inf_t.pencolor("white")
        inf_colors = ["#89CFF0", "#7393B3", "#0096FF","#6495ED","#00A36C"]
        inf_j += 1
        if inf_j >= len(inf_colors):
            inf_j = 0
        inf_t.fillcolor(inf_colors[inf_j])
        inf_t.begin_fill()
 
        inf_side_length_c = math.sqrt(2)*inf_side_length_a
        inf_h = math.sqrt((inf_side_length_c / 2) * (inf_side_length_c / 2))
        inf_t.forward(inf_h)
        inf_t.left(135)
        inf_side_length_a *= 0.5
        
        inf_t.forward(inf_side_length_a)
        inf_t.end_fill()
        inf_t.right(135)
        inf_.update()
    inf_.mainloop() 
    turtle.done()
def Venn():
    
    print("Venn was the first to create a “random walk” or “drunk walk”.  Using the decimal expansion of pi, each digit is seen as a cardinal direction. source: https://www.jeffreythompson.org/blog/2012/01/03/random-pi-walk/")
    
    Venn_t = turtle.Turtle()
    Venn_t.speed(10)
    Venn_number_of_decimals = 200
    Venn_pi = 0

    Venn_step_Size = 20
    mp.dps = Venn_number_of_decimals
    Venn_pi = mp.pi
    Venn_pi_decimalPart = Venn_pi - int(Venn_pi)
    Venn_pi_decimalPart = str(Venn_pi_decimalPart)
    Venn_get_pi_decimals = list(Venn_pi_decimalPart)
    Venn_get_pi_decimals = Venn_get_pi_decimals[2:]
    for i in Venn_get_pi_decimals:
        Venn_t.pencolor("#89CFF0")

        if int(i) == 0:
            Venn_t.setheading(90)
            Venn_t.forward(Venn_step_Size)
        elif int(i) == 1:
             Venn_t.setheading(45)
             Venn_t.forward(Venn_step_Size)
        elif int(i) == 2:
            Venn_t.setheading(0)
            Venn_t.forward(Venn_step_Size)
        elif int(i) == 3:
            Venn_t.setheading(315)
            Venn_t.forward(Venn_step_Size)
        elif int(i) == 4:
            Venn_t.setheading(270)
            Venn_t.forward(Venn_step_Size)
        elif int(i) == 5:
            Venn_t.setheading(225)
            Venn_t.forward(Venn_step_Size)
        elif int(i) == 6:
            Venn_t.setheading(180)
            Venn_t.forward(Venn_step_Size)
        elif int(i) == 7:
            Venn_t.setheading(135)
            Venn_t.forward(Venn_step_Size)
    turtle.done()
def Theodorus():



    Theo_square_root_of = 0
    Theo_factor = 50
    Theo_j = 0 
    Theo_t = turtle.Turtle()
    Theo_t.speed(10)
    for i in range(25):
        Theo_t.pencolor("white")
        Theo_colors = ["#89CFF0", "#7393B3", "#0096FF","#6495ED","#00A36C"]
        Theo_j += 1
        if Theo_j >= len(Theo_colors):
            Theo_j = 0
        Theo_t.fillcolor(Theo_colors[Theo_j])
    
        #print(fibonacci[-1])
        Theo_t.begin_fill()
        
        Theo_square_root_of += 1
       
        Theo_t.forward(math.sqrt(sTheoquare_root_of) * Theo_factor)
        Theo_t.left(90)
        Theo_t.forward(1 * Theo_factor)
        Theo_t.left(360 - 90 - (180 - math.degrees(math.atan(1/math.sqrt(Theo_square_root_of)))))
        Theo_square_root_of += 1
        Theo_t.end_fill()
        Theo_t.forward(math.sqrt(Theo_square_root_of) * Theo_factor)
        Theo_t.right(180)
    turtle.mainloop() 
    turtle.done()


    
    Yel_Yellowstone = [1,2,3]
    Yel_factor = 4
    for i in range(7000):   
        for i in range(7000):
            if math.gcd(i,Yel_Yellowstone[-1]) == 1 and math.gcd(i, Yel_Yellowstone[-2]) > 1 :
                if i in Yel_Yellowstone:
                    print("next")
                else:
                    print(i)
                    Yel_Yellowstone.append(i)
                    break
    Yel_t = turtle.Turtle()
    Yel_t.color("#89CFF0")
    Yel_t.speed(100)
    Yel_screen = Screen()
    Yel_t.penup()
    Yel_t.goto(6/2 - screen.window_width()/2, screen.window_height()/2 - 6/2)
    Yel_t.pendown()
    for i in Yel_Yellowstone:
        Yel_t.fillcolor("#89CFF0")
        Yel_t.begin_fill()
        Yel_t.right(90)
        t.forward(Yel_Yellowstone[i]* Yel_factor)
        Yel_t.left(90)
        Yel_t.forward(3)
        Yel_t.left(90)
        Yel_t.forward(Yel_Yellowstone[i] * Yel_factor)
        Yel_t.right(90)
        Yel_t.end_fill()
        turtle.update()
    turtle.mainloop() 
def Ulam():
    

    ul = turtle.Screen()
    
    print("The Ulam spiral or prime spiral is a graphical depiction of the set of prime numbers")
    #repitition = repitition
    Ul_t = turtle.Turtle()
    Ul_t.color("white", "black")
    Ul_t.clear()
    Ul_t.speed(10)
    Ul_prime = False
    Ul_t.fillcolor("#89CFF0")
    Ul_t.begin_fill()
    for _ in range(4):  
        Ul_t.forward(5)
        Ul_t.left(90) 
    Ul_t.end_fill()
    Ul_current_Number = 1
    Ul_step_Size = 5
    Ul_change_Direc = 1
    Ul_steps_in_Direction = 1
    for j in range(0,1000):
        for i in range(0,2):
            for k in range(Ul_steps_in_Direction):
                Ul_t.forward(Ul_step_Size)
                Ul_current_Number += 1
                for i in range (2, Ul_current_Number):
                    if (Ul_current_Number % i) == 0:
                        break
                else:
                    Ul_prime = True
                if Ul_prime == True:
                    Ul_t.fillcolor("#89CFF0")
                    Ul_t.begin_fill()
                    for _ in range(4):  
                        Ul_t.forward(5)
                        Ul_t.left(90) 
                    Ul_t.end_fill()
                    Ul_prime = False
            Ul_t.forward(Ul_step_Size)
       
   
            Ul_t.left(90)
        Ul_steps_in_Direction += 1
        turtle.update()
    turtle.mainloop()
    turtle.done()
