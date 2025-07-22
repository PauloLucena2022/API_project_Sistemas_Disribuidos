# Importação e Separação dos dados
import pandas as pd

previsores = pd.read_csv('dataset/dataset_base_label/predictors.csv')
labels = pd.read_csv('dataset/dataset_base_label/labels.csv')

import joblib
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
previsores = scaler.fit_transform(previsores)

joblib.dump(scaler, 'scaler_obesidade.pkl')

from sklearn.model_selection import train_test_split
previsores_treinamento, previsores_teste, labels_treinamento, labels_teste = train_test_split(previsores, labels, test_size=0.3)

# Estrutura da Rede Neural
import keras
from keras.models import Sequential
from keras.layers import Dense, Input, Dropout

classificador = Sequential()

classificador.add(Input(shape=(16,))) # entrada
classificador.add(Dense(units = 16, # camada oculta 1
                        activation = 'relu',
                        kernel_initializer = 'random_uniform'))
classificador.add(Dense(units = 8, # camada oculta 2
                        activation = 'relu',
                        kernel_initializer = 'random_uniform'))
classificador.add(Dense(units = 7, # saída
                        activation = 'softmax'))

# Configuração da rede
otimizador = keras.optimizers.Adam(learning_rate = 0.001, clipvalue = 0.5)
classificador.compile(optimizer = otimizador, 
                      loss = 'sparse_categorical_crossentropy', 
                      metrics = ['accuracy'])

# Treinamento
classificador.fit(previsores_treinamento, labels_treinamento, batch_size = 10, epochs = 100)

# Visualização dos pesos 
pesos0 = classificador.layers[0].get_weights()
pesos1 = classificador.layers[1].get_weights()
pesos2 = classificador.layers[2].get_weights()

print(f"Pesos 'Entrada -> Camada Oculta 1' {pesos0}")
print(f"Pesos 'Camada Oculta 1 -> Camada 1' {pesos1}")
print(f"Pesos 'Camada Oculta 2 -> Saída' {pesos2}")

# Previsões da Rede
from sklearn.metrics import accuracy_score

previsoes = classificador.predict(previsores_teste)
previsoes = previsoes.argmax(axis = 1)

accuracy = accuracy_score(labels_teste, previsoes)
print(f"Acurácia do modelo: {accuracy*100:.2f}%")

classificador.save('modelo_obesidade_final.h5')



