import tkinter as tk
from tkinter import filedialog # For masters task
from typing import Callable, Union, Optional
from a3_support import *
from model import *
from constants import *
import os
os.chdir(os.path.dirname(__file__))


class ItemView(tk.Frame):
    def __init__(self, master: tk.Frame, 
                 item_name: str, amount: int,
                 select_command=None, 
                 sell_command=None, 
                 buy_command=None) -> None:
         
        self.item_name = item_name
        cost = 0
        """ Creates 6 frames to display the inventory of the player, 
            which contains the name, amount, sell price and cost of buying of an item.
            the code is split into Crops and Crop seeds.
            
            An update function is implemented to update the amount after buying or selling.
        """
        
        
        #If else gets the item's name and match the corresponding amount to it
        if item_name == 'Potato':
            scost = SELL_PRICES.get(item_name,0)
            if amount == None:
                value = 0
                bgcolour = INVENTORY_EMPTY_COLOUR
            else:
                value = amount
                bgcolour = INVENTORY_COLOUR
                
            super().__init__(master,width = INVENTORY_WIDTH, 
                             bg=bgcolour)    
            itemtext = f"{item_name}: {value}\nSell price: ${scost}\nBuy price: $N/A"
            
            self.label = tk.Label(self, text=itemtext, bg= bgcolour)
            self.label.pack(side=tk.LEFT)
            
            self.buy_button = tk.Button(self, text="Sell", 
                                        command=lambda: 
                                            sell_command(self.item_name,scost))
            self.buy_button.pack(side=tk.LEFT)
                
        if item_name == 'Kale':
            scost = SELL_PRICES.get(item_name,0)
            if amount == None:
                value = 0
                bgcolour = INVENTORY_EMPTY_COLOUR
            else:
                value = amount
                bgcolour = INVENTORY_COLOUR
                
            super().__init__(master,width= INVENTORY_WIDTH, 
                             bg=bgcolour)  
            itemtext = f"{item_name}: {value}\nSell price: ${scost}\nBuy price: $N/A"
            
            self.label = tk.Label(self, text=itemtext, 
                                  bg= bgcolour)
            self.label.pack(side=tk.LEFT)
            
            self.buy_button = tk.Button(self, text="Sell", 
                                        command=lambda: 
                                            sell_command(self.item_name,scost))
            self.buy_button.pack(side=tk.LEFT)
                
        if item_name == 'Berry':
            scost = SELL_PRICES.get(item_name,0)
            if amount == None:
                value = 0
                bgcolour = INVENTORY_EMPTY_COLOUR
            else:
                value = amount
                bgcolour = INVENTORY_COLOUR
            
            super().__init__(master,width= INVENTORY_WIDTH, bg=bgcolour)  
            itemtext = f"{item_name}: {value}\nSell price: ${scost}\nBuy price: $N/A"
            
            self.label = tk.Label(self, text=itemtext, bg= bgcolour)
            self.label.pack(side=tk.LEFT)
            
            self.buy_button = tk.Button(self, text="Sell", 
                                        command=lambda: 
                                            sell_command(self.item_name,scost))
            self.buy_button.pack(side=tk.LEFT)
        
        #This portion finds the name of the item and matches the corresponding amount, cost of buying and selling price    
        else:
            for item in BUY_PRICES:
                if item == item_name: 
                    cost = BUY_PRICES.get(item, 0)
                    scost = SELL_PRICES.get(item,0)
                    
                    if amount == None:
                        value = 0
                        bgcolour = INVENTORY_EMPTY_COLOUR
                    else:
                        value = amount
                        bgcolour = INVENTORY_COLOUR
                    
                    super().__init__(master,width= INVENTORY_WIDTH, bg=bgcolour)      
                    itemtext = f"{item_name}: {value}\nSell price: ${scost}\nBuy price: ${cost}"
                
                    # Create label widget
                    self.label = tk.Label(self, text=itemtext,bg=bgcolour)
                    self.label.pack(side=tk.LEFT)
                    
                    #Sell and buy button is mapped to sell_command/buy_command
                    self.buy_button = tk.Button(self, text="Buy", 
                                                command=lambda: buy_command(self.item_name,cost))
                    self.buy_button.pack(side=tk.LEFT)
                    
                    self.sell_button = tk.Button(self,text = "Sell", 
                                                 command=lambda:sell_command(self.item_name,scost))
                    self.sell_button.pack(side=tk.LEFT)
    
                    
     

    def update(self, amount: int, selected: bool = False) -> None:
        
        
        self.label.config(text=f"{self.item_name}: {amount}\nSell price: ${self.sell_price}\nBuy price: ${self.buy_price}")





class InfoBar(AbstractGrid):
    """
        Creates the information bar at the bottom of the frame, which contains day, energy and money.
        
        Function Redraw updates the energy, money and day when the next day button is clicked
    """
    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        size = (FARM_WIDTH + INVENTORY_WIDTH, INFO_BAR_HEIGHT)
        super().__init__(master, dimensions=(2, 3), size=size)

    #Clears the existing information bar and recreates it with updated values
    def redraw(self, day: int, money: int, energy: int) -> None:
        self.clear()

        # Annotate day, money, and energy in the corresponding cells
        self.annotate_position((0, 0), "Day:", font= HEADING_FONT)
        self.annotate_position((0, 1), "Money:", font= HEADING_FONT)
        self.annotate_position((0, 2), "Energy:", font= HEADING_FONT)
        self.annotate_position((1, 0), day)
        self.annotate_position((1, 1), f"${money}")
        self.annotate_position((1, 2), energy)
       

class FarmView(AbstractGrid):
    """Creates the map plot where the farm and player exists in.
    Redraw clears and recreates the map plot with updated positions and images

    
    """
    def __init__(self, master: Union[tk.Tk, tk.Frame], 
                 dimensions: tuple[int, int], size: tuple[int, int], **kwargs) -> None:
        super().__init__(master, dimensions, size, **kwargs)
        self.image_cache = {}  
          
    def redraw(self, ground: list[str],
               plants: dict[tuple[int, int], Plant], 
               player_position: tuple[int, int], 
               player_direction: str) -> None:
        
        self.clear()
        
        for i, row in enumerate(ground):
            for j, tile in enumerate(row):
                position = self.get_midpoint((i,j))
                if str(tile) == 'G':
                    img = 'images/grass.png'
                elif str(tile) == 'U':
                    img = 'images/untilled_soil.png'
                elif str(tile) == 'S':    
                    img = 'images/soil.png'
                size = self.get_cell_size()
                image = get_image(img, size, self.image_cache)
                self.create_image(position, image= image)
                
        #Create and place the images for the plants
        for position, plant in plants.items():
            image_name = get_plant_image_name(plant)
            image = get_image(image_name, self.get_cell_size(), self.image_cache)
            self.create_image(position, image=image)

        #Create and place the image for the player
        if player_direction == 'w':
            player_image_name = 'images/player_w.png'
        elif player_direction == 'a':
            player_image_name = 'images/player_a.png'  
        elif player_direction == 's':
            player_image_name = 'images/player_s.png'
        elif player_direction == 'd':
            player_image_name = 'images/player_d.png'
            
        position = self.get_midpoint(player_position)
        
        player_image = get_image(player_image_name,
                                 self.get_cell_size(), self.image_cache)
        
        self.create_image(position, image=player_image)
        
    
        
class FarmGame():
    """Controller class that controls the different classes and map them together.
       Creates FarmView, Inforbar, Banner and ItemView instances and uses redraw
       to get all classes to redraw and update values
    """
    
    
    def __init__ (self, master: tk.Tk, 
                  map_file: str) -> None:
        self.cache = {}
        master.title("Farm Game")
        self.model = FarmModel(map_file)
        self.player = self.model.get_player()
        self.map_file = map_file
        self.plantf ={}
        self.position ={}
        self.mainframe = tk.Frame(master)
        self.mainframe.pack()
        self.viewframe = tk.Frame(self.mainframe)
        self.viewframe.pack()
        viewDimensions = self.model.get_dimensions()
        self.farmview = FarmView(self.viewframe,
                                 viewDimensions, 
                                 ((FARM_WIDTH,FARM_WIDTH)))
        title_image = get_image('images/header.png', 
                                ((FARM_WIDTH + INVENTORY_WIDTH), 
                                 BANNER_HEIGHT), self.cache)
        
        #Creates a label for the FarmGame Banner
        title_banner = tk.Label(self.viewframe, 
                                image = title_image)
        title_banner.pack()
        
        self.farmview.pack(side= tk.LEFT)
        
        #Next day button
        btn = tk.Button (self.mainframe, text= 'Next day',
                         command=self.increment_day)
        btn.pack(side=tk.BOTTOM)

        for item in ITEMS:
            self.itemview = ItemView(self.viewframe, item, 
                                     self.inv_amount(item), 
                                     self.player.sell, self.player.buy)
            self.itemview.pack(
                side= tk.TOP, expand= True, fill='both'
            )
       
        #InfoBar
        self.info_bar = InfoBar(self.mainframe)  # Instantiate InfoBar
        self.info_bar.pack(anchor='sw')  # Pack the InfoBar into the FarmGame window
        
        
        
        master.bind(
            "<KeyPress>", self.key_press
        )
        
        
        
        self.redraw()
    
    def inv_amount(self,name: str):
        inv = self.player.get_inventory()
        for item_name in inv:
            if name == item_name:
                return inv.get(item_name,0)
            
    def inv_name(self,list = dict):
        invname =self.player._inventory
        for name in invname:
            return name
        
    
    def sell_command(self,item_name, price):
        self.player.sell(item_name,price)
        list = self.player.get_inventory()
        for item in list:
            if item == item_name:    
                self.itemview.update(list.get(item,0), True)
        
    def increment_day(self):
        # Advance to the next day in the model
        self.model.new_day()
        self.redraw()
    
    def redraw(self):
        # Redraw the view classes to reflect the changes in the model
        FarmView.redraw(self.farmview, 
                        self.model._map, 
                        self.plantf, 
                        self.model.get_player_position(), 
                        self.model.get_player_direction())
       
       
        self.info_bar.redraw(self.model.get_days_elapsed(), 
                             self.player.get_money(), 
                             self.player.get_energy())
        
    def key_press(self, event: tk.Event) -> None:
        if event.char == 'w':
            direction = UP
            self.model.move_player(direction)
            
        elif event.char == 's':
            direction = DOWN
            self.model.move_player(direction)
            
        elif event.char == 'a':
            direction = LEFT
            self.model.move_player(direction)
            
        elif event.char == 'd':
            direction = RIGHT
            self.model.move_player(direction)
            
        elif event.char == 't':
            self.model.till_soil(self.model.get_player_position())
            
        elif event.char == 'u':
            self.model.untill_soil(self.model.get_player_position())
            
        else:
            return

        self.redraw()
    
  
    

def play_game(root: tk.Tk, map_file: str) -> None:
    FarmGame(root, map_file)
    root.mainloop()
    

def main() -> None:
    root = tk.Tk()
    play_game(root, 'maps/map1.txt')

if __name__ == '__main__':
    main()
