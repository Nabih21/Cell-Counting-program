# Nabih El-helou
# 260766611 
import matplotlib.pyplot as plt
import random
import os
import skimage.io as io
import numpy as np
from skimage.color import rgb2gray
from skimage.filters import sobel
from PIL import Image
import numpy as np


    
# This function is provided to you. You will need to call it.
# You should not need to modify it.
def seedfill(im, seed_row, seed_col, fill_color,bckg):
    """ Runs the seedfill algorithm
    Args:
        im (graytone image): The image on which to perform the seedfill algorithm
        seed_row (int) and seed_col (int): position of the seed pixel
        fill_color (float between 0 and 1): Color for the fill
        bckg (float between 0 and 1): Color of the background, to be filled
    Returns: 
        int: Number of pixels filled
    Behavior:
        Modifies the greytone of some pixels by performing seedfill
    """
    
    # check that the image if a greyscale image
    if type(im[0,0])!=np.float64:
        raise TypeError("This is not a greyscale image. Aborting.")

    # check that the fill_color is not the same as bckg
    if fill_color==bckg:
        raise ValueError("fill_color can't be the same as bckg")

    
    size=0  # keep track of patch size
    n_row, n_col = im.shape
    front={(seed_row,seed_col)}  # initial front
    while len(front)>0:
        r, c = front.pop()  # remove an element from front
        if im[r, c]==bckg: 
            im[r, c]=fill_color  # color the pixel
            size+=1
            # look at all neighbors
            for i in range(max(0,r-1), min(n_row,r+2)):
                for j in range(max(0,c-1),min(n_col,c+2)):
                    # if background, add to front
                    if im[i,j]==bckg and (i,j) not in front:
                        front.add((i,j))
    return size


# QUESTION 4
def fill_cells(edge_image):
    """ Fills each enclosed region with a different grayscale value
    Args:
        edge_image (grayscale): An image, with black background and
                                white edges
    Returns: 
        A new grayscale image where each close region is filled with a different
        grayscale value
    """
    seedfill(edge_image, 0, 0, 0.1, 0)
    n_regions_found_so_far= 0
    for r in range(len(edge_image)):
        for c in range(len(edge_image[0])):
            if edge_image[r][c] == 0 :
                n_regions_found_so_far += 1
                seedfill(edge_image, r, c, 0.5+0.001*n_regions_found_so_far , 0.0)
                
    return n_regions_found_so_far             
                
    
    
    # return None # REMOVE THIS LINE WHEN YOU'RE DONE


# QUESTION 5
def classify_cells(original_image, labeled_image, 
                   min_size=1000, max_size=5000, 
                   infected_grayscale=0.5, min_infected_percentage=0.02):
    """ Classifies and counts infected and non-infected cells
    Args:
        original_image (grayscale): The original gayscale image
        labeled_image (grayscale): Image where each enclosed region is colored
                       with a different grayscal value
        min_size (int), max_size (int): The min and max size of a region to be 
                                        called a cell
        infected_grayscale (float): Maximum grayscale value for a pixel to be 
                                    called infected
        min_infected_percentage (float): Smallest fraction of dark pixels 
                                         needed to call a cell infected
    Returns: 
        tuple of two sets: (grayscale values of infected cells, grayscale values
                            of uninfected cells)
    """
    grayscale_set= set()
    for r in range(len(labeled_image)):
        for c in range(len(labeled_image[0])):
            grayscale_set.add(labeled_image[r][c])
    infected=set()
    not_infected=set()
   
    for g in grayscale_set:
        dark= 0
        light= 0
        for r in range(len(labeled_image)):
            for c in range(len(labeled_image[0])):
                if g == labeled_image[r][c]:
                    
                    if original_image[r][c] <= infected_grayscale:
                        dark += 1
                    if original_image[r][c] > infected_grayscale:
                        light += 1
        
        total_pixel= dark + light            
        if min_size < total_pixel < max_size :
            if dark/total_pixel >= min_infected_percentage:
                infected.add(g)
            else:
                not_infected.add(g)
            
                   
                        
    
    return (infected, not_infected) # REMOVE THIS LINE WHEN YOU'RE DONE


# QUESTION 6
def annotate_image(color_image, labeled_image, infected, not_infected):
    """ Annotates the cells in the image, using green for uninfected cells
        and red for infected cells.
    Args: Labeled infected cells in red, and uninfected cells in green
        color_image (color image): An image of cells
        labeled_image (grayscale): Image where each closed region is colored
                       with a different grayscal value
        infected (set of float): A set of graytone values of infected cells
        not_infected (set of float): A set of graytone values of non-infcted cells
    Returns: 
        color image: An image with infected cells highlighted in red
             and non-infected cells highlighted in green
    """ 
    for r in range(len(labeled_image)-1):
        for c in range(len(labeled_image[0])-1):
            for i in range(r-1, r+2):
                for j in range(c-1, c+2):
                    if labeled_image[i][j] == 1 :
                        
                        if labeled_image[r][c] in infected:
                            color_image = color_image.convert('RGB')
                            color_image.putpixel((c, r), (255, 0, 0))
                        if labeled_image[r][c] in not_infected :
                            color_image = color_image.convert('RGB')
                            color_image.putpixel((c, r), (0, 255, 0))                               
    
    return color_image # REMOVE THIS WHEN YOU'RE DONE


if __name__ == "__main__":  # do not remove this line   


    # QUESTION 1: WRITE YOUR CODE HERE
   # image = io.imread("malaria-1.jpeg")
    # image = io.imread("malaria-1-small.jpeg")
    #image = io.imread("/Users/nabihelhelou/Desktop/Fall 2023/internship/comp204/assignment_5_comp/malaria-1.jpeg")
    image = io.imread("malaria-1.jpeg")
    gray_image = rgb2gray(image)

   
    
    sobel_mag = np.sqrt(sum([sobel(gray_image, axis=i)**2
                          for i in range(gray_image.ndim)]) / gray_image.ndim)
    plt.imshow(sobel_mag)
    plt.show()
    


    # Convert the image to 'L' mode and save
    image = Image.fromarray((sobel_mag * 255).astype(np.uint8))
    image = image.convert('L')
    image.save("Q1_Sobel.jpg")
    #io.imsave("Q1_Sobel.jpg", sobel_mag)


    # QUESTION 2: WRITE YOUR CODE HERE
    T= 0.05
    for r in range(len(sobel_mag)):
        for c in range(len(sobel_mag[0])):
            if sobel_mag[r][c] < T:
                sobel_mag[r][c] = 0
            if sobel_mag[r][c] >= T:
                sobel_mag[r][c] = 1
    
                
    
    plt.imshow(sobel_mag)    
    plt.show()  
    image = Image.fromarray((sobel_mag * 255).astype(np.uint8))
    image = image.convert('L')
    image.save("Q2_Sobel_T_0.05.jpg") 
        

    # QUESTION 3: WRITE YOUR CODE HERE
    sobel_mag_copy = sobel_mag.copy()
    n_row, n_col = sobel_mag_copy.shape
    for r in range(len(sobel_mag)):
        for c in range(len(sobel_mag[0])):
            if gray_image[r][c] == 1 :
                sobel_mag_copy[r][c]= 0
            else:
                  for i in range(max(0,r-1), min(n_row,r+2)):
                      for j in range(max(0,c-1),min(n_col,c+2)):
                          if gray_image[i][j] < 0.5:
                              sobel_mag_copy[r][c]= 0
    
    plt.imshow(sobel_mag_copy)
    plt.show()
    image = Image.fromarray((sobel_mag_copy * 255).astype(np.uint8))
    image = image.convert('L')
    image.save("Q3_Sobel_T_0.05_clean.jpg")
    #io.imsave("Q3_Sobel_T0.05_clean.jpg", sobel_mag_copy)
            

    # QUESTION 4: WRITE YOUR CODE CALLING THE FILL_CELLS FUNCTION HERE
    # breakpoint()
    edge_image = sobel_mag_copy.copy()
 
    
    N_cells = fill_cells(edge_image)
    plt.imshow(edge_image)
    plt.show()
    image = Image.fromarray((edge_image * 255).astype(np.uint8))
    image = image.convert('L')
    image.save("Q4_Sobel_T_0.05_clean_filled.jpg")
   # io.imsave("Q4_Sobel_T_0.05_clean_filled.jpg", edge_image)
    
    # QUESTION 5: WRITE YOUR CODE CALLING THE CLASSIFY_CELLS FUNCTION HERE
    cells_tuple = classify_cells(gray_image, edge_image)
    

    # QUESTION 6: WRITE YOUR CODE CALLING THE ANNOTATE_IMAGE FUNCTION HERE
    
    Final_image = annotate_image(image, edge_image , cells_tuple[0] , cells_tuple[1])
    
    
    plt.imshow(Final_image)
    plt.show()
    
    