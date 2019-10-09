# arbol_binario.py
# Autor: Dorian Vallecillo
# Descripción: Librería que incluye diversas funciones para implementar un árbol binario


import queue

# Contiene la información de cada nodo del árbol binario
class Nodo:
    def __init__(self, val=None):
        self.valor = val
        self.left = None
        self.right = None


# Implementa funciones para crear y realizar operaciones sobre un árbol binario
class ArbolBinario:
    def __init__(self):
        self.root = None

    #######################################
    # "Interfaz" de la clase ArbolBinario #
    #######################################

    # Crea un arbol desde el archivo especificado
    def crear_desde_archivo(self, nombre):
        try:
            handle = open(nombre, "r")
        except IOError:
            return None

        self.root = self._crear_desde_archivo(handle)

        handle.close()

        if self.root is None:
            return None
        return 1

    # Retorna True si el árbol está vacío y False en caso contrario
    def esta_vacio(self):
        return self.root is None

    # Retorna la altura del árbol
    def altura(self):
        if self.root is None:
            return -1
        return self._altura(self.root)

    # Imprime el recorrido del árbol en PreOrden
    def recorrido_pre_orden(self):
        self._pre_orden(self.root)

    # Imprime el recorrido del árbol EnOrden
    def recorrido_en_orden(self):
        self._en_orden(self.root)

    # Imprime el recorrido del árbol en PosOrden
    def recorrido_pos_orden(self):
        self._pos_orden(self.root)

    # Imprime el recorrido del árbol por Niveles
    def recorrido_por_nivel(self):
        self._orden_por_nivel(self.root)

    # Imprime el recorrido del árbol por Niveles - Versión recursiva
    def _orden_por_nivel(self, actual):
        niveles = self._altura(actual) + 1
        for i in range(1, niveles):
            self._orden_por_nivel_recursivo(actual, i)

    # Auxiliar para el recorrido del árbol en Level-Order
    def _orden_por_nivel_recursivo(self, actual, nivel):
        if actual is None:
            return
        if nivel == 1:
            print(actual.valor + ' ')
        else:
            self._orden_por_nivel_recursivo(actual.left, nivel-1)
            self._orden_por_nivel_recursivo(actual.right, nivel-1)
    # Imprime el recorrido del árbol en Level-Order (Breadth-first search) ITERATIVO
    # Utiliza la misma técnica que Insertar. Sin embargo, se recorren todos los nodos
    def recorrido_por_nivel_iterativo(self):
        if self.root is None:
            return

        cola = queue.Queue()

        cola.put(self.root)
        while not cola.empty():
            tmp = cola.get()
            print(tmp.valor + ' ')
            if tmp.left is not None:
                cola.put(tmp.left)
            if tmp.right is not None:
                cola.put(tmp.right)

    # Inserta un nuevo nodo en el árbol. Encuentra el primer espacio disponible en un nivel del árbol
    def insertar(self, val):
        # Utilizamos una cola para almacenar los nodos en cada nivel
        cola = queue.Queue()

        # Si el árbol está vacío, se crea el nodo y se convierte en raíz
        if self.root is None:
            self.root = Nodo(val)
            return

        # Avanzamos por el subárbol izquierdo y derecho almacenando cada elemento en la cola
        # Luego se van recuperando en orden FIFO. De esa manera, la primer posición desocupada
        # en un dado nivel se usa para el Nodo nuevo
        cola.put(self.root)
        while not cola.empty():
            tmp = cola.get()
            if tmp.left is not None:
                cola.put(tmp.left)
            else:
                tmp.left = Nodo(val)
                return

            if tmp.right is not None:
                cola.put(tmp.right)
            else:
                tmp.right = Nodo(val)
                return

    # Retorna True si la llave existe en el árbol, False si no la encuentra
    def buscar(self, key):
        if self._buscar(self.root, key) is not None:
            return True
        return False

    # Elimina el nodo dado por la llave
    # El algoritmo funciona de la siguiente manera:
    #    a) Encontramos el nodo que hay que eliminar
    #    b) Obtenemos la dirección del nodo con mayor profundidad
    #    c) Copiamos los datos del nodo más profundo al nodo que se eliminará
    #    d) Eliminamos al nodo con mayor profundidad
    #    Nota: La eficiencia de este algoritmo puede mejorar
    def eliminar(self, key):
        # Obtenemos el nodo que deseamos borrar
        tmp = self._buscar(self.root, key)

        # Si no existe el nodo con la llave terminamos
        if tmp is None:
            return

        # Obtenemos el nodo con mayor profundidad
        ultimo = self._nodo_mas_profundo()

        # Si solamente existe un nodo en el árbol lo eliminamos
        if self.root == ultimo:
            self.root = None
            return

        # Si el nodo a eliminar y el más profundo son diferentes, copiamos los datos
        if tmp != ultimo:
            tmp.valor = ultimo.valor

        # Procedemos a borrar el nodo más profundo utilizando un procedimiento similar a insertar
        cola = queue.Queue()

        cola.put(self.root)
        while not cola.empty():
            tmp = cola.get()

            # Comparmos el nodo izquierdo con el último y lo eliminamos si coincide
            if tmp.left is not None:
                if tmp.left == ultimo:
                    tmp.left = None
                    return
                cola.put(tmp.left)

            # Comparmos el nodo derecho con el último y lo eliminamos si coincide
            if tmp.right is not None:
                if tmp.right == ultimo:
                    tmp.right = None
                    return
                cola.put(tmp.right)

    # Elimina el árbol completamente
    def borrar_arbol(self):
        self.root = None

    ####################################
    # Funciones auxiliares de la clase #
    ####################################

    # Función auxiliar para crear un árbol binario tipo char desde el archivo manejado por handle
    def _crear_desde_archivo(self, handle):
        c = handle.read(1)

        if c == '$':
            return None

        tmp = Nodo(c)

        tmp.left = self._crear_desde_archivo(handle)
        tmp.right = self._crear_desde_archivo(handle)

        return tmp

    # Función auxiliar para recorrer el árbol y retornar la altura
    def _altura(self, actual):
        if actual is None:
            return 0

        maxizq = self._altura(actual.left)
        maxder = self._altura(actual.right)

        if maxizq > maxder:
            return maxizq + 1
        return maxder + 1

    # Función auxiliar para el recorrido en PreOrden
    def _pre_orden(self, actual):
        if actual is not None:
            print(actual.valor + ' ')
            self._pre_orden(actual.left)
            self._pre_orden(actual.right)

    # Función auxiliar para el recorrido EnOrden
    def _en_orden(self, actual):
        if actual is not None:
            self._en_orden(actual.left)
            print(actual.valor + ' ')
            self._en_orden(actual.right)

    # Función auxiliar para el recorrido en PosOrden
    def _pos_orden(self, actual):
        if actual is not None:
            self._pos_orden(actual.left)
            self._pos_orden(actual.right)
            print(actual.valor + ' ')

  

    # Auxiliar para el recorrido del árbol en Level-Order
    def recorrido_por_nivel_recursivo(self, actual, nivel):
        if actual is None:
            return
        if nivel == 1:
            print(actual.valor + ' ')
        else:
            self.recorrido_por_nivel_recursivo(actual.left, nivel-1)
            self.recorrido_por_nivel_recursivo(actual.right, nivel-1)

    # Retorna un apuntador al Nodo que contenga la llave
    # None si no encuentra la llave
    def _buscar(self, actual, key):
        # Si el árbol está vacío, retornamos None
        if actual is None:
            return None

        # Si el elemento existe en el Nodo, retornamos el apuntador al Nodo
        if actual.valor == key:
            return actual

        tmp = self._buscar(actual.left, key)

        if tmp is not None:
            return tmp
        else:
            return self._buscar(actual.right, key)

    # Retorna el nodo con mayor profundidad en el árbol. Utiliza la misma técnica que insertar.
    # Sin embargo, se recorren todos los nodos hasta llegar al que se encuentre con mayor profundidad
    def _nodo_mas_profundo(self):
        if self.root is None:
            return None

        tmp = None
        cola = queue.Queue()

        cola.put(self.root)
        while not cola.empty():
            tmp = cola.get()
            if tmp.left is not None:
                cola.put(tmp.left)
            if tmp.right is not None:
                cola.put(tmp.right)
        return tmp
        
    def _InOrden_Iterativo(self):

        stack=  queue.LifoQueue()
        actual=self.root
        while actual is not None:
            stack.put(actual)
            actual=actual.left
        while stack.empty() is False:
            izquierdo=stack.get()
            print( izquierdo.valor) 
            print( izquierdo.right.valor)
            izquierdo=stack.get()
            derecho=izquierdo.right
            print(izquierdo.valor)
            print( derecho.valor)
            izquierdo=stack.get()
            print( izquierdo.valor)
            print( izquierdo.right.left.valor)
            print( izquierdo.right.valor)
            print( izquierdo.right.right.left.valor)
            print(izquierdo.right.right.valor)
            print(izquierdo.right.right.right.valor)
            
    def pre_orden_iterativo(self,actual):
        aux=actual
        pila=queue.LifoQueue()
        while True:
            if aux is not None:
                print(aux.valor)
                pila.put(aux)
                aux=aux.left
            elif pila.empty() is not True:
                aux=pila.get()
                aux=aux.right
            condicion=False
            if(pila.empty==False and aux is not None):
                condicion=True
            if(condicion):
                break
        
    def compararListas(self,NodoA, NodoB):
        ListaA= list()
        ListaB= list()
        actual1=NodoA
        actual2=NodoB
        self.pos_orden_lista(actual1, ListaA)
        self.pos_orden_lista(actual2, ListaB)
        sizeA=len(ListaA)
        sizeB=len(ListaB)
        if(sizeA != sizeB):
            return False
        else:
            for i in range(sizeA):
                valorA=ListaA.pop()
                valorB=ListaB.pop()
                if(valorA!=valorB):
                    return False
            return True

    def espejo(self, entrante):
        nodito=entrante
        if nodito is None:
            return
        else:
            tmp=nodito
            self.espejo(nodito.left)
            self.espejo(nodito.right)
            tmp= nodito.left
            nodito.left=nodito.right
            nodito.right=tmp

        arbol=ArbolBinario()
        arbol.root=nodito
        return arbol      

    def esEspejo(self, NodoA, NodoB):
        actual1=self.espejo(NodoA)
        actual2=NodoB
        salida=self.compararListas(actual1.root,actual2)
        return salida

    def nodo_mas_grande(self):
        actual=self.root
        lista=list()
        self.pos_orden_lista(actual,lista)
        size=len(lista)
        if(size>0):
            mayor=lista.pop()
            size=len(lista)
            for i in range(size):
                aux=lista.pop()
                if(aux.valor>mayor.valor):
                    mayor=aux
        return mayor        

    def pos_orden_lista(self,actual, lista):
       if actual is not None:
            self.pos_orden_lista(actual.left,lista)
            lista.append(actual)
            self.pos_orden_lista(actual.right, lista)

    def _hojas(self, actual, hojitas):
        if actual is not None:
            self._hojas(actual.left,hojitas)
            if(actual.left is None and actual.right is None):
                hojitas.append(actual)
            self._hojas(actual.right,hojitas)

    def hojas(self):
        actual=self.root
        hojitas=list()
        self._hojas(actual, hojitas)
        hojas=len(hojitas)
        return hojas
    def cuentaNodos(self):
        lista=list()
        actual=self.root
        self.pos_orden_lista(actual,lista)
        size=len(lista)
        return size
   
    

if __name__ == '__main__':
    arbolito=ArbolBinario()
    arbolito.crear_desde_archivo("arbolchar.txt")
    print("Arbol Normal")
    arbolito.recorrido_pos_orden()
    print("--------------------")
    espejo=arbolito.espejo(arbolito.root)
    print("Arbol Espejo del Normal")
    espejo.recorrido_pos_orden()
    var=arbolito.esEspejo(arbolito.root, espejo.root)
    if(var is True):
        print("Son Espejos")
    else:
        print("No son Espejos")
    print("Cantidad de Hojas: "+ espejo.hojas().__str__())
    print("Cantidad de Nodos: "+ espejo.cuentaNodos().__str__())
    print("Nodo mas Grande: " + espejo.nodo_mas_grande().valor)

 