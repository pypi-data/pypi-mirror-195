import numpy as np #Для операций линейной алгебры
import pandas as pd #Для считывания данных
from sklearn.mixture import GaussianMixture #Для определения нечётких переменных методом гаусовых смесей
from sklearn.preprocessing import StandardScaler  #для нормализации данных
from sklearn.metrics import mean_squared_error,accuracy_score #для оценки ошибки
from matplotlib import pyplot as plt #для построения графиков ошибок
import time #для измерения времени
import itertools #Для получения декартова произведения при формировании правил
from Activation_functions import ActFuncs as FA#Набор функций активации и лямбда-функций
from inspect import signature #для определения количества аргументов в функции
from sklearn.mixture import GaussianMixture #Для опеределения числа нп
from dataclasses import dataclass,field
from typing import Callable,List
from sklearn.model_selection import train_test_split #Для деления выборки на тестовую и обучающую
import warnings

@dataclass
class Layer:
    Neurons_count: int #Число нейронов слоя
    ActFunc: Callable  = FA.SIGMOID #Функция активации
    logical: bool = True #Ограничить ли веса слоя диапазоном значений [0,1]
    blinking: bool = False #Учитывать ли при вычислении выхода слоя пришедшие np.nan значения?
    I: np.ndarray = True #Маска наличия связей
    R: np.ndarray = True #Маска обучаемости связей
    Recent_entires: List[np.ndarray] = field(default_factory=list) #Последние входы для рассчёта градиента
    
    def output(self,x):
        return self.ActFunc.value[0](self.I*(np.isfinite(x) | (not self.blinking)).reshape(-1,1),x,*self.W)
            
    def correction(self,h,Antigradient, L1=0, L2=0): #антиградиент пришедший справа(от следующего слоя)
        delta_W = np.full(self.W.shape, 0.0)
        delta_X = np.empty((Antigradient.shape[0],self.W.shape[1]))
        
        for i,Ant in enumerate(Antigradient): #проходимся по всем наблюдениям
            x = self.Recent_entires[i]
            warnings.filterwarnings('ignore','divide by zero') #игнорируем ошибки с делением на 0
            warnings.filterwarnings('ignore', 'invalid value encountered in') #игнорируем ошибки с NaN
            (diff_ActFunc_x,diff_ActFunc_w) = self.ActFunc.value[1](self.I*(np.isfinite(x) | (not self.blinking)).reshape(-1,1),x,*self.W) #Производная активационной функции
            
            delta_W +=  np.nan_to_num(self.I *diff_ActFunc_w * Ant,copy=False,nan=0.0,posinf=0.0,neginf=0.0)
            delta_X[i] = np.nan_to_num((self.I * diff_ActFunc_x) @ Ant,copy=False,nan=0.0,posinf=0.0,neginf=0.0)
            
        self.W -= h * self.R * self.I * (delta_W + ((L2 * 2*self.W + L1 * np.sign(self.W)) if not self.logical else 0))

        if self.logical:
            self.W = np.clip(self.W,0,1)
        self.Recent_entires = []
        return delta_X #передаём градиент на следующий слой

class Network:
    def __init__(self,Inputs,Layers:list[Layer], Classification = False) -> None:
        self.Classification = Classification
        self.Layers = Layers
        for i,layer in enumerate(self.Layers):
            parametrs_count = len(signature(layer.ActFunc.value[0]).parameters)-2
            layer.W =np.random.random((parametrs_count, self.Layers[i-1].Neurons_count if i>0 else Inputs, self.Layers[i].Neurons_count)) # матрица весов
            
    def predict(self,x):
        for слой in self.Layers: #Вычисляем прогноз по каждому слою для данного набора
            слой.Recent_entires = x #Запоминаем последний вход слоя(заменить на усреднение всех входов текущего обучения)
            x = np.apply_along_axis(слой.output ,axis=1,arr=x) # Вычисляем выход слоя #new_x = слой.Выход_слоя(new_x)
        return x
    
    def fit(self,X,Y, h = 1, batch_size = None, max_iterations = 100, min_error = 0.01, L1 = 0.0, L2 = 0.00):       
        Errors = []
        Errors_test = []
        #X = StandardScaler().fit_transform(X)
        batch_size = X.shape[0] - 1 if batch_size is None else batch_size #Если размер батча не указан - используем всю выборку
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=batch_size, random_state=42)
        
        while(True):
            Y_pred_test = self.predict(X_test)
            notnan_test = np.isfinite(Y_pred_test).all(axis=1)
            Y_pred_train = self.predict(X_train)
            notnan_train = np.isfinite(Y_pred_train).all(axis=1)
            
            if  np.sum(notnan_train) > 0:
                if not self.Classification:
                    Error = mean_squared_error( Y_pred_train[notnan_train],Y_train[notnan_train]) #Считаем функцию ошибки 
                    Error_test = mean_squared_error(Y_pred_test[notnan_test],Y_test[notnan_test]) #Считаем функцию ошибки 
                    Gradient = np.nan_to_num(Y_pred_train - Y_train,copy=False,nan=0)*2/np.sum(notnan_train)
                else:
                    Error = 0
                    Error_test = 0
                    for ind, value in np.ndenumerate(Y_train):
                        Error += (np.argmax(Y_pred_train[ind[0]]) != round(value))*(1 - 2*Y_pred_train[ind[0],round(value),0] + np.sum(Y_pred_train[ind[0]]))
                    for ind, value in np.ndenumerate(Y_test):
                        Error_test += (np.argmax(Y_pred_test[ind[0]]) != round(value))*(1 - 2*Y_pred_test[ind[0],round(value),0] + np.sum(Y_pred_test[ind[0]]))
                    
                    Error =  Error/np.sum(notnan_train) 
                    Error_test = Error_test/np.sum(notnan_test) #Считаем функцию ошибки 
                
                    Gradient = np.empty((Y_pred_train.shape[0],1))
                    for ind, value in np.ndenumerate(Y_train):
                        Gradient[ind] = Y_pred_train[ind[0],round(value)]-np.max(Y_pred_train[ind[0]])
                    Gradient = np.nan_to_num(Gradient,nan = 0)/np.sum(notnan_train)
                
                for layer in reversed(self.Layers):         
                    Gradient = layer.correction(h,Gradient,L1,L2) #корректируем слои
            else:
                Error = np.nan
                Error_test = np.nan    
            Errors.append(Error)
            Errors_test.append(Error_test)
            print(f"{len(Errors)}:{Errors[-1]}")
            if (max_iterations is not None and len(Errors) >= max_iterations) or (Error <= min_error):  #Условия остановки цикла обучения  
                break
            
        return Errors
    @staticmethod
    def construct(Data):
        Y =  Data[:,0:1] #Предсказываемый признак в первом столбце
        X =  Data[:,1:] #Входные переменные в остальных столбцах

        #region Рассчёт количества НП для каждой ЛП
        количество_нп = []
        centers = []
        warnings.filterwarnings('ignore','Number of distinct clusters') #игнорируем предупреждения о числе кластеров
        for i in range(Data.shape[1]):
            bics = []
            means = []
            for j in range(1,3):
                gmm = GaussianMixture(n_components= j, covariance_type="full")
                gmm.fit(Data[:,i].reshape(-1,1))
        
                bics.append(gmm.bic(Data[:,i].reshape(-1,1)))
                means.append(gmm.means_[:,0])
            количество_нп.append(np.argmin(bics) + 1)
            centers.append(means[np.argmin(bics)])
        количество_нп_x = количество_нп[1:]
        центры_x = centers[1:]
        количество_нп_y = 2*количество_нп[0]
        центры_y = centers[:1]
        индексы_нп_x = []
        последний_индекс = -1
        for i in количество_нп_x:
            индексы_нп_x.append(list(range(последний_индекс+1,последний_индекс+i+1)))
            последний_индекс = последний_индекс+i
        #endregion 
        #region Построение матрицы связей первого слоя
        I0 = np.zeros((X.shape[1],np.sum(количество_нп_x)),dtype=bool)
        for i,переменные in enumerate(индексы_нп_x):
            I0[i,переменные] = True  
        #endregion
        #region Получение матрицы связей второго слоя
        комбинации_нп = list(itertools.product(*индексы_нп_x))
        I1 = np.zeros((np.sum(количество_нп_x),len(комбинации_нп)),dtype=bool)
        for index,comb in enumerate(комбинации_нп):
            I1[:,index][list(comb)] = True
        #endregion
        print(f"входов:{I0.shape[0]} нп_x:{np.sum(количество_нп_x)} правил:{I1.shape[1]} нп_y:{np.sum(количество_нп_y)}")
        
        Net = Network(
                X.shape[1],
                [ 
                Layer(I1.shape[0],R=False,I=I0,ActFunc=FA.GAUSS,logical=False), #Входные НП
                Layer(I1.shape[1],R=True,I = I1,ActFunc=FA.AND,blinking=True), # Агрегирование
                Layer(количество_нп_y,R=True,ActFunc=FA.OR, blinking=True), #Активизация и композиция
                Layer(1,ActFunc= FA.LINEAR,logical = False), #Аккумуляция и дефаззификация
                ])
        for правило,переменные in enumerate(индексы_нп_x):
            Net.Layers[0].W[0,правило,переменные] = np.sort(центры_x[правило]) #задание центров функций принадлежности
            Net.Layers[0].W[1,правило,переменные] = 0.5 #задание дисперсий функций принадлежности
        return Net
    
def Тест_регрессоров():
    Data = np.array(pd.read_excel("Данные.xlsx","Заданная_функция1")) #Считываем данные из экселя
    Net = Network.construct(Data)
    модели = {
    "ANFIS_U":Network(
                X.shape[1],
                [ 
                Layer(I1.shape[0],R=False,I=I0,ActFunc=FA.GAUSS,logical=False), #Входные НП
                Layer(I1.shape[1],R=True,I = I1,ActFunc=FA.AND,blinking=True), # Агрегирование
                Layer(y_count,R=True,ActFunc=FA.OR, blinking=True), #Активизация и композиция
                Layer(1,ActFunc= FA.LINEAR,logical = False), #Аккумуляция и дефаззификация
                ]),
    "RBF":Network(
                X.shape[1],
                [ 
                Layer(I1.shape[0],I=I0,ActFunc=FA.GAUSS,logical=False), #Входные НП
                Layer(1,ActFunc= FA.LINEAR, logical = False), #Аккумуляция и дефаззификация
                ]),
    
        }
    lin = Network(
                X.shape[1],
                [ 
                #Layer(y_count,I=I0,ActFunc=FA.GAUSS,logical=False), #Входные НП
                Layer(2,ActFunc= FA.AND, I = np.array([[False,True],[True,True]])), #Аккумуляция и дефаззификация
                Layer(1,ActFunc= FA.LINEAR, logical = False), #Аккумуляция и дефаззификация
                ])
    lin.fit(X,Y, h = 0.1, max_iterations = 1000,min_error=0.00, L1=0.000,L2=0.000,batch_size=30)
    AND = lin = Network(
                X.shape[1],
                [ 
                Layer(1,ActFunc= FA.AND), #Аккумуляция и дефаззификация
                ])
    AND.fit(X,Y, h = 0.01, max_iterations = 1000,min_error=0.00, L1=0.000,L2=0.000,batch_size=30)       

    время = []
    ошибки1 =[]
    for name in модели:
        t1 = time.time()
        ошибки1.append(модели[name].fit(X,Y, h = 0.1,
                max_iterations = 1000,min_error=0.00, L1=0.000,L2=0.000,batch_size=30))
        время.append((time.time()-t1)/X.shape[0])

    i = 0.1 #портим i-ую часть значений X
    индексы_батча = np.random.choice(np.arange(X.shape[0]),size = round(i*X.shape[0]),replace=False) 
    X[индексы_батча,0] = np.nan
    ошибки2 = []
    for name in модели:
        ошибки2.append(модели[name].fit(X,Y, h = 0.1,
                max_iterations = 1000,min_error=0.00, L1=0.001,L2=0.001,batch_size=30))
    [plt.plot(ошибки1[arr],label=list(модели.keys())[arr]) for arr in range(len(ошибки1))]
    plt.legend()
    return np.array([[arr[-1] for arr in ошибки1],[arr[-1] for arr in ошибки2]])
    
def Тест_классификаторов():
    (X,Y,I0,I1,x_centers,y_count,indexes_x) = construct()
    
    I0 = np.array([
        [True,True,True,False,False,False],
        [False,False,False,True,True,True]])
    R0 = np.array([
    [
    [False,False,False,False,False,False],
    [False,False,False,False,False,False],   
    ],
    [
    [True,True,True,False,False,False],
    [False,False,False,True,True,True],   
    ]
        ])
    I1 = np.array([
    [True,True,True,False,False,False,False,False,False],
    [False,False,False,True,True,True,False,False,False],
    [False,False,False,False,False,False,True,True,True],
    [True,False,False,True,False,False,True,False,False],
    [False,True,False,False,True,False,False,True,False],
    [False,False,True,False,False,True,False,False,True]
               ])
    I1 = np.array([
    [True,True,False,False,False,False,False],
    [False,False,True,True,True,False,False],
    [False,False,False,False,False,True,True],
    [False,False,True,False,False,True,False],
    [True,False,False,True,False,False,True],
    [False,True,False,False,True,False,False]
               ])
    I2 = np.array([
    [True,True,False], #Низкий рост и Низкий вес = ? (нижняя граница нормы)
    [False,True,True], #Низкий рост и Нормальный вес = Ожирение
    [False,True,True], #Низкий рост и Высокий вес = Ожирение 
    [True,True,False], #Нормальный рост и Низкий вес = Дефицит
    [False,True,False], #Нормальный рост и Нормальный вес = Норма
    [False,True,True], #Нормальный рост и Высокий вес = Ожирение
    [True,True,False], #Высокий рост и Низкий вес = Дефицит
    [True,True,False], #Высокий рост и Нормальный вес = Норма
    [False,True,True], #Высокий рост и Высокий вес = ? (верхняя граница нормы)
    ]) 
    I2 = np.array([
    #[True,True,False], #Низкий рост и Низкий вес = ? (нижняя граница нормы)
    [False,False,True], #Низкий рост и Нормальный вес = Ожирение
    [False,False,True], #Низкий рост и Высокий вес = Ожирение 
    [True,False,False], #Нормальный рост и Низкий вес = Дефицит
    [False,True,False], #Нормальный рост и Нормальный вес = Норма
    [False,False,True], #Нормальный рост и Высокий вес = Ожирение
    [True,False,False], #Высокий рост и Низкий вес = Дефицит
    [False,True,False], #Высокий рост и Нормальный вес = Норма
    #[False,True,True], #Высокий рост и Высокий вес = ? (верхняя граница нормы)
    ]) 

    Classificator = Network(
                X.shape[1],
                [
                Layer(I0.shape[1],I = I0,R=False,ActFunc=FA.GAUSS,logical=False), #Входные НП
                Layer(I1.shape[1],I = I1,ActFunc=FA.AND,blinking=True), # Агрегирование
                Layer(I2.shape[1],I = I2,ActFunc=FA.OR,blinking=True), # Активизация и композиция
                Layer(1,ActFunc=FA.SOFTMAX, blinking=True), #Аккумуляция и вывод
                ],Classification=True)

    центры_рост = [1.5 + x*(2 - 1.5)/2 for x in range(3)]
    b_рост = 0.1
    центры_вес = [41 + x*(120 - 41)/2 for x in range(3)]
    b_вес = 13.0
    Classificator.Layers[0].W = np.array([
    [
    [центры_рост[0],центры_рост[1],центры_рост[2],0,0,0],
    [0,0,0,центры_вес[0],центры_вес[1],центры_вес[2]],   
    ],
    [
    [b_рост,b_рост,b_рост,0,0,0],
    [0,0,0,b_вес,b_вес,b_вес],   
    ]
    ])
    Ошибка2 = Classificator.fit(X,Y, h = 1.15, max_iterations = 10000,min_error=0.00, L1=0.00,L2=0.0)
    return Ошибка2   

Тест_регрессоров()
#Тест_классификаторов()
(X,Y,I0,I1,x_centers,y_count,indexes_x) = construct()

Classificator = Network(
                X.shape[1],
                [
                Layer(I0.shape[1],I = I0,R=True,ActFunc=FA.GAUSS,logical=False), #Входные НП
                Layer(I1.shape[1],I = I1,R=True, ActFunc=FA.AND,blinking=True), # Агрегирование
                Layer(y_count,I = True,R=True, ActFunc=FA.OR,blinking=True), # Активизация и композиция
                Layer(1,ActFunc=FA.SOFTMAX, blinking=True), #Аккумуляция и вывод
                ],Classification=True)
#Classificator.fit(X,Y,30,max_iterations=1000,min_error=0.0)
print(f"{ANF.predict(np.array([[1.7,51]]))[0]} : {Classificator.predict(np.array([[1.7,51]]))[0]}")