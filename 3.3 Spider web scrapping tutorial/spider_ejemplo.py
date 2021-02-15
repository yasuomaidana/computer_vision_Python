#!/usr/bin/env python
# coding: utf-8

# ## Spider tutorial
# https://www.w3schools.com/xml/xpath_syntax.asp
# Notacion Xpath
# 

# In[5]:


__author__='Yasuo'
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader


# In[6]:


class Pregunta(Item):
    pregunta= Field()
    id = Field() #Numero de pregunta

class StackOverSpider(Spider): #para web scrappers sencillos es de clase Spider
    name="MiPrimerSpider"
    start_urls=['https://stackoverflow.com/questions'] #En forma de lista, como es sencillo sera de 1 solo elemento
    def parse(self,response): #response esta en formato xml es la respuesta de la web es invocada por el framework
        sel=Selector(response) #selector
        #ver imagen
        preguntas = sel.xpath('//div[@id="questions"]/div') #acepta otros formatos como css
        ##preguntas es de tipo lista
        
        #Iterar sobre preguntas
        for i,element in enumarate(preguntas):
            item=ItemLoader(Pregunta(),element)#recibe clase de estructura del item y elemento donde se tiene el xpath
            item.add_xpath('pregunta','.//h3/a/text()')#campo al que queremos agregar el xpath
            item.add_value('id',i)
            yield item.load_item()


# In[7]:


#Inser image into jupyter #![image.png](estWeb.png)


# ![image.png](estWeb.png)
# ![image.png](pregWeb.png)
# 

# yield is a keyword in Python that is used to return from a function without destroying the states of its local variable and when the function is called, the execution starts from the last yield statement

# ## Running spider
# 

# In[8]:



# In[12]:




# In[ ]:




