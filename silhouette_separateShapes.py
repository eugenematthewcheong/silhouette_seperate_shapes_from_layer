# -*- coding:utf-8 -*-

from fx import *
import os
import fx
from tools.objectIterator import ObjectIterator

def sanitycheck(selections):
  check = True
  for s in selections:
    if s.isType("Layer"):
        check = False
  
  return check
    

def seperateShapesfunc(selections):
  labellist = []
  chosenLayers = []
  
  for s in selections:
    labellist.append(s.label)
  
  for s in selections:
    root = False
    p = s.parent
    while root == False:
        if p.parent.isType("Node"):
          if not p.label in chosenLayers:
            chosenLayers.append(p.label)
            
            rootlayer = p
            root = True
          else:
            if not p.label in chosenLayers:
              chosenLayers.append(p.label)
              p = p.parent
              root = False
  
  new_layer = rootlayer.clone()
  new_layer.label = uniqueLabel(new_layer.label)
  
  current = new_layer.children
  rejected = []
  newfoundlayers = []
  
  
  for num, i in enumerate(current):
    if i.isType("Layer"): #first layer
      newfoundlayers.append(i)
      newCurrent = i.children
      for shape in newCurrent:
        if shape.isType("Shape") and shape.label in labellist:
            if num == len(current):
              break
            else:
               continue
          
          
        elif shape.isType("Layer"): #second layer
          newfoundlayers.append(shape)
          newerCurrent = shape.children
          for newshape in newerCurrent:
            if newshape.isType("Shape") and newshape.label in labellist:
              if num == len(current):
                break
              else:
                 continue
            
            elif newshape.isType("Layer"): #third layer
              newfoundlayers.append(newshape)
              newererCurrent = newshape.children
              for newershape in newererCurrent:
                if newershape.isType("Shape") and newershape.label in labellist:
                  if num == len(current):
                    break
                  else:
                    continue

                else:
                  rejected.append(newershape)
                  continue
                    


            else:
              rejected.append(newshape)
              continue


        else:
          rejected.append(shape)
          continue

            
    elif i.isType("Shape") and i.label in labellist:
        if num == len(current):
            break
        else:
            continue
    else:
        rejected.append(i)
        continue


  layersleft = []
  for layer in newfoundlayers:
    if layer.label not in chosenLayers:
        layersleft.append(layer)
        
  
  
  beginUndo("Seperating Shapes with Layers")
  new_layer.property("objects").removeObjects(rejected)
  new_layer.property("objects").removeObjects(layersleft)
  activeNode().property("objects").addObjects([new_layer])

  endUndo()


class seperateShapes(Action):
  def __init__(self):
    Action.__init__(self, 'EM Tools | Separate Shapes')
    
    def execute(self):
      selections = selection()
      if sanitycheck(selections) == True:
        try:
          seperateShapesfunc(selections)
        except:
          fx.displayWarning("Unable to separate shapes")
          pass
      else:
        fx.displayWarning("Select Shapes only")
        

        
addAction(seperateShapes())